from __future__ import annotations

from videos.music.music63.common import *  # noqa: F403
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
        d = load("tune63")
        c = clip("tune.variation63")
        st = d["starts"]
        keys = d["names"]
        f = d["found"]
        head = VGroup(label(r"Variation 63", font_size=48, color=TUNE), label(r"five noisy seconds, \ named", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup()
        for k, row in zip(keys, f):
            ok = row["found"] == row["truth"]
            name = (row["found"] or "nothing").split("/")[-1]
            cells.add(VGroup(RoundedRectangle(width=3.6, height=1.3, corner_radius=0.12, stroke_color=TUNE if ok else EAR, fill_opacity=0),
                             VGroup(label(name, font_size=17, color=TUNE if ok else EAR),
                                    label(rf"{row['votes']} votes, \ at {row['offset_s']:.1f} s" if row["offset_s"] is not None else r"no match", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.12)).arrange(ORIGIN))
        cells.arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)
        note = label(r"three earlier Variations in a noisy bar, \ the music 3 dB above the noise; \ each named after it is heard", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here are five noisy "
            "seconds from each of three earlier Variations, chosen at random, in a bar where the music is only three decibels "
            "above the noise. After each, the fingerprinter's answer appears."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"Variation 63", kind="physical model", detail=r"three Variations, \ a simulated bar", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                progress = VGroup(Line(LEFT * 1.65, RIGHT * 1.65, color=GREY_A, stroke_width=2), Dot(radius=0.09, color=WHITE)).move_to(cells[i].get_bottom() + DOWN * 0.18)
                def advance(m, tt, begin=st[k], stop=end):
                    fraction = np.clip((tt - begin) / max(stop - begin, 0.01), 0, 1)
                    m[1].move_to(m[0].get_start() + fraction * (m[0].get_end() - m[0].get_start()))
                    m.set_opacity(1.0 if begin <= tt < stop else 0.0)
                snd.show(progress)
                snd.drive(progress, advance)
                snd.show(cells[i])
                snd.drive(cells[i], lambda m, t, s1=end: (m.set_opacity(1.0 if t >= s1 - 0.6 else 0.15), m[0].set_fill(opacity=0)))
        self.add(cells)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row sixty-three of the ledger: {v['measure']}. The ledger is now also a library, and these three chosen excerpts were found under the demonstrated noise conditions."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"fingerprints: \ spectrogram peaks paired into hashes; \ votes agree in time",
            r"they survive noise and codecs, \ and identify recordings, \ not songs",
            r"chance matches scatter; \ thresholds need empirical calibration",
            r"embeddings describe sound; \ a classifier can learn a hum instead of the music",
            r"implicit ALS fits profiles from plays; \ content rescues new songs",
            r"popularity feeds on itself; \ exploring and fairness push back",
        ], title=r"What we found", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Fingerprints pair spectrogram peaks into hashes, and true matches agree in time. <bookmark mark='a'/> They survive noise and codecs, and identify recordings, not songs. <bookmark mark='b'/> Chance matches scatter, but correlated music and multiple comparisons require empirical threshold calibration. <bookmark mark='c'/> Embeddings describe sound, and a classifier can learn a hum instead of the music. <bookmark mark='d'/> Implicit matrix factorization fits profiles from plays, and the sound rescues songs nobody has played. <bookmark mark='e'/> And popularity feeds on itself, while exploring and fairness push back."
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
            r"A query has 300 hashes; \ the library 50 million; \ hashes are 24 bits. \ How many chance hits? \ Spread over a million clip-offsets, \ how many per bin?",
            r"Show that with confidences $c_{ui}$ fixed, \ each ALS step solves a weighted least-squares problem exactly, \ so the loss never increases.",
            r"\textbf{Ear.} \ The lab plays queries at several noise levels; \ guess where the fingerprinter fails, \ then check.",
            r"\textbf{Build.} \ Add exploration by Thompson sampling to the feedback loop, \ and measure inequality and recall.",
            r"$\bigstar$ \ How much of the change in music over the streaming era did recommenders cause?",
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
            (r"source separation: \ which instruments a mix contains", [64]),
            (r"machines that compose: \ memorization tests by matching", [65]),
            (r"generative audio: \ detecting generated tracks", [66]),
            (r"research: \ benchmarks, \ horses and honest evaluation", [67]),
            (r"the concert: \ the Variations in one playlist", [68]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In source separation, asking which instruments a mix contains. In machines that "
            "compose, testing for memorization by matching. In generative audio, detecting generated tracks. In research, "
            "with benchmarks, horses and honest evaluation. And in the concert, the Variations in one playlist."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"identify", r"fingerprints for recordings; \ chroma matching for songs"),
            (r"evaluate", r"split by artist and studio; \ test what should not matter"),
            (r"recommend", r"beat popularity before claiming success; \ explore"),
            (r"name", r"ISRCs and ISWCs on every file, \ linked"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Identify recordings with fingerprints and songs with chroma matching. Evaluate with splits by "
            "artist and studio, and test what should not matter. Beat the popularity baseline before claiming a recommender "
            "works, and explore. And name everything: codes on every file, linked."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"M. Müller, \ \textit{Fundamentals of Music Processing} \ (2nd ed., \ 2021)",
             r"O. Celma, \ \textit{Music Recommendation and Discovery} \ (2010)",
             r"M. Schedl et al., \ `Current challenges and visions in music recommender systems research' \ (2018)",
             r"B. L. Sturm, \ `The GTZAN dataset: \ its contents, \ its faults, \ their effects on evaluation' \ (2013)",
             r"P. Knees and M. Schedl, \ \textit{Music Similarity and Retrieval} \ (2016)"],
            [r"A. Wang, \ `An industrial-strength audio search algorithm' \ (ISMIR, \ 2003)",
             r"Y. Hu, \ Y. Koren and C. Volinsky, \ `Collaborative filtering for implicit feedback datasets' \ (ICDM, \ 2008)",
             r"B. L. Sturm, \ `A simple method to determine if a music information retrieval system is a horse' \ (2014)",
             r"G. Tzanetakis and P. Cook, \ `Musical genre classification of audio signals' \ (2002)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 63, "2023: a 1970s cassette",
            "Can a mix be un-mixed, and how would we know how well?",
            "2023: a voice is lifted off a home cassette from the 1970s, away from the piano recorded on the same "
            "track, and a finished song is built around it. <bookmark mark='a'/> Can a mix be un-mixed, and how would "
            "we know how well? <bookmark mark='b'/> Next time. Part 64: Source Separation.",
            signoff=clip("bridge.signoff"))
