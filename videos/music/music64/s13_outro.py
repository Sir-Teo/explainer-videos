from __future__ import annotations

from videos.music.music64.common import *  # noqa: F403
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
        d = load("tune64")
        c = clip("tune.variation64")
        st = d["starts"]
        keys = d["names"]
        names = {"acap_sep": (r"a cappella, \ separated", TUNE), "kara_sep": (r"karaoke, \ separated", TUNE),
                 "acap_true": (r"a cappella, \ true stems", GREY_B), "kara_true": (r"karaoke, \ true stems", GREY_B)}
        head = VGroup(label(r"Variation 64", font_size=48, color=TUNE), label(r"un-mixed", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(RoundedRectangle(width=2.8, height=1.2, corner_radius=0.12, stroke_color=names[k][1]),
                                label(names[k][0], font_size=16, color=names[k][1])).arrange(ORIGIN) for k in keys]).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.2)
        note = label(r"the session's Tune: \ the voice alone, \ then the band without it; \ first from the network, \ then from the stems as recorded", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here the session's Tune "
            "is un-mixed: the voice alone, and the band without it, first as the network separates them, then from the stems "
            "as they were recorded."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"Variation 64", kind="physical model", detail=r"Part 56's session, \ the network", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune64")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row sixty-four of the ledger: the separated voice {say(d['sdr_voice'], 1)} decibels from the truth, the karaoke "
            f"{say(d['sdr_karaoke'], 1)}. The karaoke scores higher because what it lacks, the voice, is a small part of it, "
            "though its mistakes are just as audible."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"one channel, \ many sources: \ separation needs assumptions",
            r"panning and centre cancellation; \ ICA, \ perfect when dry, \ lost in a room",
            r"median filters split harmonic from percussive; \ NMF uses each source's templates",
            r"source-informed reference masks: \ ideal binary and ratio",
            r"the mixture's phase is the error no mask removes",
            r"a network needs data, \ and a leaked test flatters it; \ SDR is not the ear",
        ], title=r"What we found", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? With one channel and many sources, separation needs assumptions. <bookmark mark='a'/> Panning and centre cancellation work in stereo; ICA can recover sources under its instantaneous independence assumptions and can fail on reverberant mixtures. <bookmark mark='b'/> Median filters split harmonic from percussive, and NMF uses each source's own templates. <bookmark mark='c'/> Ideal binary and ratio masks are useful source-informed references, not universal performance ceilings. <bookmark mark='d'/> Nonnegative real-valued masks retain the mixture phase; complex masks can change it. <bookmark mark='e'/> A network is only as good as its data, and a test that shares the training data flatters it. And SDR is not the ear: it cannot tell leakage from artifacts."
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
            r"A source is panned at $\theta = 70^\circ$ by a sine-cosine law. \ What is its panning index, \ and how much of it survives $L - R$?",
            r"Show that the ideal ratio mask minimizes the squared error of a masked estimate when the sources' phases agree in every bin.",
            r"\textbf{Ear.} \ The lab plays separations at several SDRs, \ some by leakage and some by artifacts; \ rank them, \ then check.",
            r"\textbf{Build.} \ Train the network on all four stems at once, \ and compare its drums with the median filter's.",
            r"$\bigstar$ \ Can a metric rank separators as listeners do, \ including generative ones that invent?",
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
            (r"machines that compose: \ stems as training material", [65]),
            (r"generative audio: \ separation by generation; \ voices and rights", [66]),
            (r"research: \ listening tests for separation", [67]),
            (r"the concert: \ the Variations as stems", [68]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In machines that compose, which train on stems. In generative audio, with separation by "
            "generation, and voices and their rights. In research, with listening tests. And in the concert at the end, where "
            "the Variations come apart into their stems."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"stereo first", r"if sources are panned apart, \ use it"),
            (r"report", r"SDR and SI-SDR, \ with the oracle masks beside them"),
            (r"listen", r"leakage and artifacts sound different at the same score"),
            (r"rights", r"a separated stem is still the recording"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. If the sources are panned apart, use that first. Report SDR and its scale-invariant cousin, with "
            "the oracle masks beside them. Listen, because leakage and artifacts sound different at the same score. And remember "
            "that a separated stem is still the recording, rights and all."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"E. Vincent, \ T. Virtanen and S. Gannot \ (eds.), \ \textit{Audio Source Separation and Speech Enhancement} \ (2018)",
             r"Z. Rafii et al., \ `An overview of lead and accompaniment separation in music' \ (IEEE/ACM TASLP, \ 2018)",
             r"A. S. Bregman, \ \textit{Auditory Scene Analysis} \ (1990)",
             r"A. Hyvärinen, \ J. Karhunen and E. Oja, \ \textit{Independent Component Analysis} \ (2001)"],
            [r"D. FitzGerald, \ `Harmonic/percussive separation using median filtering' \ (DAFx, \ 2010)",
             r"J. Le Roux et al., \ `SDR: \ half-baked or well done?' \ (ICASSP, \ 2019)",
             r"Z. Rafii et al., \ `The MUSDB18 corpus for music separation' \ (2017)",
             r"A. Défossez et al., \ `Music source separation in the waveform domain' \ (2019)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 64, "Oregon, 1997",
            "What does a machine that composes know?",
            "1997: an audience in Oregon hears three pieces, one by Bach, one by a music professor in Bach's style, "
            "and one by a program. <bookmark mark='a'/> They pick the program's as the real Bach. What does a machine "
            "that composes know? <bookmark mark='b'/> Next time. Part 65: Machines that Compose.",
            signoff=clip("bridge.signoff"))
