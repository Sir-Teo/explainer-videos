from __future__ import annotations

from videos.music.music58.common import *  # noqa: F403
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
        d = load("tune58")
        c = clip("tune.variation58")
        st = d["starts"]
        keys = d["names"]
        names = {"k128": (r"128", TUNE), "k64": (r"64", TUNE), "k32": (r"32", BLUE), "k24": (r"24", EAR), "k16": (r"16", EAR), "residue": (r"what 32 threw away", GREY_A)}
        head = VGroup(label(r"Variation 58", font_size=48, color=TUNE), label(r"five bit rates, \ and the residue", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(RoundedRectangle(width=1.95 if k != "residue" else 3.0, height=1.2, corner_radius=0.12, stroke_color=names[k][1]),
                                label(names[k][0] + (r" \ kbit/s" if k != "residue" else ""), font_size=16, color=names[k][1])).arrange(ORIGIN) for k in keys]).arrange(RIGHT, buff=0.2).move_to(DOWN * 0.2)
        note = label(rf"our session playing the Tune, \ through Monochord's coder; \ then the difference between the original and the 32 kbit/s version, \ turned up 10 dB", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here our session plays it "
            "through our coder at five bit rates, from a hundred and twenty-eight kilobits down to sixteen; and then you hear "
            "what the thirty-two kilobit version threw away, alone."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"Variation 58", kind="physical model", detail=r"our session, \ Monochord's coder", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune58")
        r = {row["kbps"]: row for row in d["rows"]}
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row fifty-eight of the ledger. From a hundred and twenty-eight kilobits, where the noise sits {say(r[128]['margin'])} "
            f"decibels under the mask, to sixteen, where it is {say(-r[16]['margin'])} decibels over it. And the residue, heard "
            "alone, is a ghostly copy of the music: everything the coder decided you would not miss."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"entropy bounds lossless coding; \ prediction and Rice codes reach about half",
            r"a masking model gives each band of each frame its allowed noise",
            r"the MDCT overlaps by half yet sends N numbers for N samples: \ its aliases cancel",
            r"step sizes from the mask, \ one margin from the bit rate; \ short blocks against pre-echo; \ mid-side",
            r"ABX tests count, \ and need many trials to find a subtle difference",
            r"generations compound errors; \ vector quantization leads to neural codecs",
        ], title=r"What we found", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Entropy bounds lossless coding, and prediction with Rice codes reaches about half the size. "
            "<bookmark mark='a'/> A masking model gives each band of each frame the noise it can hide. <bookmark mark='b'/> The "
            "MDCT overlaps its frames by half yet sends N numbers for N samples, because its aliases cancel. "
            "<bookmark mark='c'/> Step sizes come from the mask, one margin from the bit rate; short blocks fight pre-echo, and "
            "mid-side saves bits. <bookmark mark='d'/> ABX tests count right answers, and need many trials to find a subtle "
            "difference. <bookmark mark='e'/> Generations compound errors, and vector quantization leads to the neural codecs."
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
            r"A coefficient's band allows noise of power $10^{-4}$ per coefficient. \ What step size puts the noise exactly there, \ and 6 dB under?",
            r"Show that the MDCT's window must satisfy $w_n^2 + w_{n+N}^2 = 1$ for the aliases to cancel.",
            r"\textbf{Ear.} \ The lab codes a voice at random rates and plays them; \ order them by bit rate.",
            r"\textbf{Build.} \ Add window switching to the coder: \ short blocks when an attack is detected, \ with start and stop windows.",
            r"$\bigstar$ \ Can a learned metric predict ratings for a kind of codec that did not exist when it was trained?",
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
            (r"live sound: \ low-delay codecs on stage and online", [59]),
            (r"the business of music: \ the files that changed it", [60]),
            (r"finding music: \ fingerprints that survive a codec", [63]),
            (r"generative audio: \ codec tokens as an alphabet", [66]),
            (r"research: \ listening tests and their statistics", [67]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In live sound, with low-delay codecs on stage and online. In the business of music, "
            "changed by these files. In finding music, with fingerprints that survive a codec. In generative audio, which writes "
            "in codec tokens. And in research, with listening tests and their statistics."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"archiving", r"lossless masters; \ every lossy file made once, \ from them"),
            (r"delivery", r"AAC or Opus at 128 kbit/s or more for music; \ $-1$ dBTP"),
            (r"judging", r"blind, \ level-matched, \ enough trials, \ and the hidden reference"),
            (r"listening", r"a lone voice or castanets: \ the hardest test of any codec"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Keep lossless masters, and make every lossy file from them, once. Deliver music in AAC or Opus at "
            "a hundred and twenty-eight kilobits or more, with a true-peak margin. Judge codecs blind, level-matched, with "
            "enough trials and a hidden reference. And test them on a lone voice or castanets, useful stress material alongside varied music and listening conditions."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"M. Bosi and R. E. Goldberg, \ \textit{Introduction to Digital Audio Coding and Standards} \ (2003)",
             r"J. Sterne, \ \textit{MP3: \ The Meaning of a Format} \ (2012)",
             r"K. Brandenburg, \ `MP3 and AAC explained' \ (AES, \ 1999)",
             r"T. Painter and A. Spanias, \ `Perceptual coding of digital audio' \ (Proc. IEEE, \ 2000)"],
            [r"J. P. Princen and A. B. Bradley, \ `Analysis/synthesis filter bank design based on time domain aliasing cancellation' \ (1986)",
             r"J. D. Johnston, \ `Transform coding of audio signals using perceptual noise criteria' \ (1988)",
             r"J.-M. Valin et al., \ `High-quality, \ low-delay music coding in the Opus codec' \ (AES, \ 2013)",
             r"N. Zeghidour et al., \ `SoundStream: \ an end-to-end neural audio codec' \ (2021)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 58, "August 1965",
            "Why does a microphone howl, and why are loudspeakers hung in curves?",
            "August 1965: fifty-five thousand people fill a baseball stadium, and nobody, the band included, can hear "
            "the band. <bookmark mark='a'/> Why does a microphone howl, and why are loudspeakers hung in curves? "
            "<bookmark mark='b'/> Next time. Part 59: Live Sound.")
