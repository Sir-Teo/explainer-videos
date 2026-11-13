from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403
from videos.music.variations import rows_before

NAMES = ("A", r"B$\flat$", "B", "C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$")


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune")
        v = load("variation")
        c = clip("tune.variation4")
        head = VGroup(label(r"Variation 4", font_size=48, color=TUNE),
                      label(r"the notes the ear supplies", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.4)
        amps = np.array([0.001, 0.001, 1.0, 0.8, 0.6, 0.45])
        bars = partial_bars(amps, width=4.6, height=2.2, db=False).move_to(LEFT * 3.4 + UP * 0.45)
        slot = 4.6 / 6
        ghosts = VGroup(*[DashedVMobject(Rectangle(width=slot * 0.62, height=2.2, stroke_color=GREY_B, stroke_width=1.5), num_dashes=24)
                          .move_to(bars.base.get_left() + RIGHT * slot * (k + 0.5) + UP * 1.1) for k in range(2)])
        bl = label(r"partials 3 to 6 only: \ nothing at the note, \ or at its octave", font_size=22, color=GREY_A).next_to(bars, UP, buff=0.25)
        circ = Circle(radius=1.25, color=GREY_C, stroke_width=2).move_to(RIGHT * 3.6 + UP * 0.45)
        names = VGroup(*[label(n, font_size=22, color=GREY_A).move_to(circ.get_center() + 1.6 * np.array([np.sin(TAU * k / 12), np.cos(TAU * k / 12), 0]))
                         for k, n in enumerate(NAMES)])
        hand = Line(circ.get_center(), circ.get_center() + UP * 1.25, color=TUNE, stroke_width=5)
        cl = label(r"the pitch heard", font_size=22, color=GREY_A).next_to(circ, UP, buff=0.6)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built a listener, "
            "so the Variation is made of things that only a listener can supply. <bookmark mark='a'/> For the "
            "first four phrases, every note has its third, fourth, fifth and sixth partials, and nothing else. "
            "There is no energy at the note, and none at its octave. <bookmark mark='b'/> The dial shows which "
            "note is meant. Then, for the last two phrases, the notes become Shepard's tones: every octave at "
            "once, so that the Tune has its notes, but no height at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(ghosts), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(circ), FadeIn(names), FadeIn(hand), FadeIn(cl))
        words, phrase, k_in = None, -1, 0
        mode = label(r"missing fundamentals", font_size=30, color=TUNE).move_to(DOWN * 1.55)
        self.add(mode)
        with self.listen(c) as snd:
            window(snd, r"Variation 4", kind="synthesized", detail=r"partials 3 to 6; \ then Shepard tones", tag_corner=DR)
            for k, nt in enumerate(c.notes):
                snd.wait_until(f"n{k}")
                if nt["phrase"] != phrase:
                    phrase, k_in = nt["phrase"], 0
                    ns = [m["name"] for m in c.notes if m["phrase"] == phrase]
                    new = VGroup(*[label(t, font_size=40, color=GREY_D) for t in ns]).arrange(RIGHT, buff=0.7).move_to(DOWN * 2.45)
                    if words is not None:
                        self.remove(words)
                    words = new
                    self.add(words)
                    if phrase == 4:
                        self.remove(mode)
                        mode = label(r"Shepard tones: \ every octave at once", font_size=30, color=EAR).move_to(DOWN * 1.55)
                        self.add(mode)
                        for b in bars.bars:
                            b.set_opacity(0.1)
                        ghosts.set_opacity(0.15)
                t0 = nt["t"]
                if nt["kind"] == "missing":
                    for j, b in enumerate(bars.bars):
                        if j >= 2:
                            snd.drive(b, lambda m, t, t0=t0, j=j: m.set_opacity(0.3 + 0.65 * float(np.exp(-(1.2 + 0.5 * j) * max(t - t0, 0)))))
                ang = TAU * ((12 * np.log2(nt["hz"] / 27.5)) % 12) / 12
                hand.put_start_and_end_on(circ.get_center(), circ.get_center() + 1.25 * np.array([np.sin(ang), np.cos(ang), 0]))
                hand.set_color(TUNE if nt["kind"] == "missing" else EAR)
                words[k_in].set_color(TUNE if nt["kind"] == "missing" else EAR)
                k_in += 1
                self.play(hand.animate(rate_func=there_and_back).set_stroke(width=9), run_time=min(0.4, nt["dur"] * 0.7))
        rows = rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}]
        led = variations_ledger(rows, highlight=(len(rows) - 1,)).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            f"Row four of the ledger. {say(v['seconds'])} seconds. We gave each of the first four phrases' notes to "
            f"Monochord's pitch model, and it placed every missing fundamental within a cent of the note that was "
            f"meant, although the strongest thing at that frequency was {say(abs(d['loudest_at_f0_db']))} decibels "
            "down. You heard a tune that, in the usual sense, was not played."
        ):
            self.play(FadeOut(words), FadeOut(mode), FadeOut(bl), FadeOut(cl), VGroup(bars, ghosts).animate.scale(0.6).shift(UP * 0.9),
                      VGroup(circ, names, hand).animate.scale(0.6).shift(UP * 0.9), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        w = load("wave")
        m = load("outer")["middle"]
        card = objectives_card([
            rf"the middle ear matches air to fluid: \ pressure $\times\,{m['pressure_gain']:.0f}$, \ {m['gain_db']:.0f} dB",
            rf"a travelling wave sorts frequency by place: \ equal ratios, \ equal distances ({w['mm_per_octave']:.1f} mm an octave in our model)",
            r"the ear's filters are a little over a whole tone wide, \ wider in the bass; \ a loud sound hides its neighbours",
            r"loudness is compressed: \ ten times the power is twice as loud",
            r"pitch is a period, \ read from the timing of the nerve up to 4 or 5 kHz; \ so a note survives without its fundamental",
            r"the living cochlea amplifies: \ sharp, \ compressive, \ and it makes tones of its own",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? The middle ear is a transformer that matches air to fluid. <bookmark mark='a'/> In "
            "the cochlea a travelling wave sorts frequency by place, and equal ratios of frequency are equal "
            "distances. <bookmark mark='b'/> The ear's filters are a little over a whole tone wide, wider in the "
            "bass, and a loud sound hides its neighbours. <bookmark mark='c'/> Loudness is compressed: ten times "
            "the power is twice as loud. <bookmark mark='d'/> Pitch is a period, read from the timing of the "
            "nerve, up to four or five thousand hertz. That is why a note survives the loss of its fundamental, "
            "and why notes stop where the piano stops. <bookmark mark='e'/> And the living cochlea is an "
            "amplifier: sharp, compressive, and noisy enough to make tones of its own."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, r in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A concert measures 103 dBA where you stand. \ For how long is it safe? \ You put in earplugs that take off 15 dB: "
            r"how long now, \ and by what factor did the time grow?",
            r"An amplifier's response is proportional to the cube root of the force. \ Show that 100 dB of input becomes 33 dB of output, \ "
            r"and that its gain rises by 20 dB for every 30 dB that the sound falls.",
            r"\textbf{Ear.} \ The lab plays a sound with partials at 900, 1200 and 1500 Hz, \ then pure tones at 300 and at 600 Hz. \ "
            r"Which pure tone has its pitch? \ Then all three partials are moved up 50 Hz: \ does the pitch rise or fall?",
            r"\textbf{Build.} \ Run \texttt{ear.pitch} on every note of Variation 4 and plot its errors. \ Then lower the model's "
            r"limit on nerve timing (\texttt{corner}) from 1200 Hz to 600 Hz, \ and to 300 Hz. \ Which notes does it lose first?",
            r"$\bigstar$ \ Build a cochlear-implant simulator: \ a bank of $N$ bands, \ each replaced by noise with the band's envelope. \ "
            r"How many bands does Monochord's pitch model need to follow the Tune? \ What does that predict for implant users?",
        ], font_size=24)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, "
            "marked with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"critical bands, \ beats and roughness", [5, 6]),
            (r"the pitch the ear supplies: \ roots", [5, 13]),
            (r"masking", [41, 56, 58]),
            (r"phons, \ sones and loudness meters", [57]),
            (r"pitch by autocorrelation", [61]),
            (r"chroma and octave equivalence", [12, 62]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? Critical bands and roughness are the whole foundation of Part 5, on "
            "consonance, and of tuning after it. The pitch that the ear supplies becomes the root of a chord. "
            "Masking returns when we orchestrate, when we mix, and when we compress audio for the ear. Loudness "
            "returns in mastering. And when we build machines that listen, they will find pitch the way this "
            "part's model does, and represent notes by their chroma."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"audiologists", r"the hearing test, \ the ear's own emissions, \ and fitting hearing aids that compress as the cochlea did"),
            (r"codec engineers", r"a model of masking decides where every bit of an audio file is spent"),
            (r"mixing engineers", r"equal-loudness curves: \ a mix balanced loud sounds thin when played quietly"),
            (r"instrument and loudspeaker designers", r"small boxes imply bass with partials, \ and let the listener supply the rest"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. An audiologist reads the ear's own emissions, and fits hearing aids that compress "
            "sound the way the lost amplifier did. A codec engineer lets a model of masking decide where every "
            "bit is spent. A mixing engineer knows that a mix balanced at high volume sounds thin when played "
            "quietly, because the ear's sensitivity to bass depends on level. And designers of small loudspeakers "
            "imply bass notes with partials, and let the listener supply the rest."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"B. C. J. Moore, \ \textit{An Introduction to the Psychology of Hearing} \ (6th ed., 2012)",
             r"C. J. Plack, \ \textit{The Sense of Hearing} \ (3rd ed., 2018)",
             r"J. O. Pickles, \ \textit{An Introduction to the Physiology of Hearing} \ (4th ed., 2012)",
             r"W. M. Hartmann, \ \textit{Signals, Sound, and Sensation} \ (1997)"],
            [r"T. Gold, \ ``Hearing. II. The physical basis of the action of the cochlea'', \ \textit{Proc. R. Soc. B} 135 (1948)",
             r"D. T. Kemp, \ ``Stimulated acoustic emissions from within the human auditory system'', \ \textit{JASA} 64 (1978)",
             r"D. D. Greenwood, \ ``A cochlear frequency-position function for several species'', \ \textit{JASA} 87 (1990)",
             r"B. R. Glasberg and B. C. J. Moore, \ ``Derivation of auditory filter shapes from notched-noise data'', \ \textit{Hear. Res.} 47 (1990)",
             r"J. C. R. Licklider, \ ``A duplex theory of pitch perception'', \ \textit{Experientia} 7 (1951)",
             r"R. N. Shepard, \ ``Circularity in judgments of relative pitch'', \ \textit{JASA} 36 (1964)",
             r"S. G. Kujawa and M. C. Liberman, \ ``Adding insult to injury'', \ \textit{J. Neurosci.} 29 (2009)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        c = clip("next.pairs")
        bx = boxes((r"lengths 2 : 3", r"lengths 32 : 45"), buff=1.2, width=3.6, height=1.5, font_size=34).move_to(UP * 1.0)
        with self.voiceover(
            "One last sound. Two strings sounding together, twice. The first time their lengths are as two to "
            "three. The second time, as thirty-two to forty-five."
        ):
            self.play(FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"two strings together, \ twice", detail=r"Part 1's string", corner=DL, tag_corner=DR)
            for ev, b in zip(("fifth", "tritone"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.2)
        nxt = VGroup(label(r"Part 5", font_size=34, color=GREY_B), label(r"Consonance", font_size=54, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The first pair is smooth. The second is rough. Pythagoras would say: small numbers, large numbers. "
            "But numbers do not make sounds rough. Ears do, and now you know how: partials that fall inside one "
            "band of the cochlea. <bookmark mark='a'/> With a string, a spectrum and an ear, we can finally ask "
            "the oldest question in music, and compute the answer. Why do some notes belong together? That is "
            "Part 5: Consonance."
        ) as vo:
            verdict = VGroup(label(r"smooth", font_size=32, color=GOOD).next_to(bx[0], DOWN, buff=0.25), label(r"rough", font_size=32, color=BAD).next_to(bx[1], DOWN, buff=0.25))
            self.play(FadeIn(verdict))
            vo.wait_until("a")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
