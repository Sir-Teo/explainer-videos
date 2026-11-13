from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403
from videos.music.variations import rows_before


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
        c = clip("tune.variation2")
        fills = {k["degree"]: k["fill"] for k in d["checks"]}
        head = VGroup(label(r"Variation 2", font_size=48, color=TUNE),
                      label(r"the Tune on six bottles", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        head.to_edge(UP, buff=0.4)
        row = bottle_row(fills, height=2.9, gap=0.75).move_to(UP * 0.35)
        ml = VGroup(*[label(rf"{k['ml']:.0f} ml" if k["ml"] > 0.5 else r"empty", font_size=24, color="#7FB3FF").next_to(row.by[k["degree"]], DOWN, buff=0.12)
                      for k in d["checks"]])
        hz = VGroup(*[label(rf"{k['hz']:.0f} Hz", font_size=22, color=FREQ).next_to(m, DOWN, buff=0.08) for k, m in zip(d["checks"], ml)])
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built air in a "
            "bottle. <bookmark mark='a'/> So here are six bottles of the same shape, each holding the amount of "
            "water that the two-tube formula asks for, <bookmark mark='b'/> from empty up to about two thirds full. "
            "Each one is struck on the mouth. This is Variation 2."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(row))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in ml], lag_ratio=0.15), LaggedStart(*[FadeIn(h) for h in hz], lag_ratio=0.15), run_time=2.0)
        words = None
        with self.listen(c) as snd:
            window(snd, r"Variation 2")
            phrase, k_in, prev = -1, 0, None
            for k, n in enumerate(c.notes):
                snd.wait_until(f"n{k}")
                if n["phrase"] != phrase:
                    phrase, k_in = n["phrase"], 0
                    names = [m["name"] for m in c.notes if m["phrase"] == phrase]
                    new = VGroup(*[label(t, font_size=40, color=GREY_D) for t in names]).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.55)
                    new.shift(RIGHT * 1.6)
                    if words is not None:
                        self.remove(words)
                    words = new
                    self.add(words)
                p = puff(row, n["degree"])
                snd.show(p)
                snd.drive(p, ring(at=n["t"], rate=6.0, stop_at=n["t"] + 1.0))
                if prev is not None:
                    row.by[prev][-1].set_color(GREY_B)
                row.by[n["degree"]][-1].set_color(TUNE)
                prev = n["degree"]
                words[k_in].set_color(TUNE)
                k_in += 1
        rows = rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}]
        led = variations_ledger(rows, highlight=(len(rows) - 1,)).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"Row two of the ledger. {say(v['seconds'])} seconds, six bottles, and every bottle within "
            f"{say(max(d['worst_cents'], 1.0))} cent of its note. Sixty-six rows to go."
        ):
            self.play(FadeOut(words), FadeOut(ml), FadeOut(hz), row.animate.scale(0.75).shift(UP * 0.9), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"sound is a push handed from parcel to parcel: \ the air stays, \ the pressure pattern travels",
            r"its speed comes from the gas law: \ $c = \sqrt{\gamma P / \rho}$, \ set by temperature alone",
            r"level in decibels: \ $+3$ dB is twice the power, \ $+6$ dB twice the pressure, \ $-6$ dB per doubling of distance",
            r"wavelength decides what a wall does: \ long waves bend round it, \ short ones are shadowed; \ two sources stripe the room",
            r"a pipe has the notes $n\,c/2L$ (open) or $(2n-1)\,c/4L$ (stopped); \ a bottle is a mass on a spring",
            r"sound is handed on where impedances match; \ a moving source shifts its pitch; \ a loud wave steepens",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Sound is a push, handed from each parcel of air to the next. The air stays; the "
            "pattern travels. <bookmark mark='a'/> Its speed comes out of the gas law and depends on temperature "
            "alone. <bookmark mark='b'/> Level is counted in decibels: three for twice the power, six for twice the "
            "pressure, and six lost for every doubling of distance. <bookmark mark='c'/> Wavelength decides what an "
            "obstacle does, and two sources stripe a room with loud and quiet. <bookmark mark='d'/> A pipe has a "
            "ladder of notes, complete if it is open, odd-numbered if it is stopped, and a bottle is a mass on a "
            "spring. <bookmark mark='e'/> Sound passes where impedances match, shifts in pitch when the source "
            "moves, and steepens when it is loud enough."
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
            r"An organ pipe, \ open at both ends, \ sounds 440 Hz at $20^\circ$C. \ How long is it (ignore the end "
            r"correction)? \ What does it sound at $10^\circ$C, \ and how many cents flat is that?",
            r"Derive Helmholtz's formula from the mass of the air in the neck and the adiabatic stiffness of the "
            r"air in the body, \ and show that it is the long-wavelength limit of "
            r"$\tan(kL_n)\tan(kL_b) = A_n / A_b$.",
            r"\textbf{Ear.} \ The lab plays a horn passing three times. \ Put the passes in order of speed, \ and "
            r"estimate the fastest from the interval it falls by.",
            r"\textbf{Build.} \ Give \texttt{air.tube} a side hole (a short open branch) and find where to drill "
            r"one in a 60 cm pipe to raise its note by a whole tone.",
            r"$\bigstar$ \ Model a trombone's bore with nonlinear propagation and a radiating bell, \ and predict "
            r"the playing level at which its spectrum turns brassy.",
        ], font_size=24)
        with self.voiceover(
            "Five problems. One to compute, one to derive, one for your ears, one to build, and one research "
            "problem, marked with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"the decibel, \ and why ten players are not ten times as loud", [4, 57]),
            (r"pipes, \ end corrections, \ odd and even partials", [8]),
            (r"Helmholtz resonators", [7, 8, 54]),
            (r"impedance and radiation", [7, 54]),
            (r"diffraction and interference", [55, 59]),
            (r"the 2-D simulator", [9, 55]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? The decibel is with us for the rest of the series, and Part 4 asks what the "
            "ear makes of it. Pipes and their end corrections are Part 8, where we build a flute, a clarinet and a "
            "voice. Helmholtz's resonator is inside the guitar of Part 7 and the loudspeaker of Part 54. And the "
            "simulator that drew this part's pictures will design a concert hall in Part 55."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"wind players and tuners", r"three cents a degree: \ warm the instrument, \ then tune"),
            (r"live sound engineers", r"six decibels per doubling; \ bass goes round the crowd, \ treble does not; \ "
             r"two speakers stripe the room"),
            (r"instrument and loudspeaker makers", r"end corrections, \ ports and sound holes, \ flares and bells"),
            (r"acoustic consultants", r"barriers by Maekawa's chart; \ simulation where the chart runs out"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A wind player warms the instrument before tuning, because of three cents a degree. A "
            "live sound engineer plans for six decibels per doubling and knows the treble will not reach behind a "
            "pillar. Makers of instruments and loudspeakers work with end corrections, ports and flares. And "
            "anyone who designs a noise barrier starts from the chart our simulation matched."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"L. E. Kinsler, A. R. Frey, A. B. Coppens and J. V. Sanders, \ \textit{Fundamentals of Acoustics} \ (4th ed., 2000)",
             r"A. D. Pierce, \ \textit{Acoustics} \ (3rd ed., 2019)",
             r"T. D. Rossing, F. R. Moore and P. A. Wheeler, \ \textit{The Science of Sound} \ (3rd ed., 2002)",
             r"N. H. Fletcher and T. D. Rossing, \ \textit{The Physics of Musical Instruments} \ (1998), ch.\ 6--8"],
            [r"G. J. Symons (ed.), \ \textit{The Eruption of Krakatoa and Subsequent Phenomena} \ (Royal Society, 1888)",
             r"H. Levine and J. Schwinger, \ ``On the radiation of sound from an unflanged circular pipe'', \ \textit{Phys. Rev.} 73 (1948)",
             r"Z. Maekawa, \ ``Noise reduction by screens'', \ \textit{Applied Acoustics} 1 (1968)",
             r"E. Fubini, \ ``Anomalie nella propagazione di onde acustiche di grande ampiezza'', \ \textit{Alta Frequenza} 4 (1935)",
             r"A. Hirschberg, J. Gilbert, R. Msallam and A. P. J. Wijnands, \ ``Shock waves in trombones'', \ \textit{JASA} 99 (1996)",
             r"G. W. Swift, \ ``Thermoacoustic engines'', \ \textit{JASA} 84 (1988)"],
            font_size=22)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        d = load("tubes")
        bars = VGroup(partial_bars(np.array(d["quiz_partials"]["B"]), width=4.2, height=1.8, db=False),
                      partial_bars(np.array(d["quiz_partials"]["A"]), width=4.2, height=1.8, db=False)).arrange(RIGHT, buff=1.4).move_to(UP * 1.0)
        tags = VGroup(label(r"an open pipe", font_size=28, color=GREY_A).next_to(bars[0], UP, buff=0.2),
                      label(r"a stopped pipe, \ same note", font_size=28, color=GREY_A).next_to(bars[1], UP, buff=0.2))
        nxt = VGroup(label(r"Part 3", font_size=34, color=GREY_B), label(r"The Spectrum", font_size=54, color=TUNE)
                     ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Twice now we have explained a sound by taking it apart. A plucked string was a stack of partials. Two "
            "pipes played the same note, and you told them apart by which partials were there. <bookmark mark='a'/> "
            "We have been leaning on that idea without ever justifying it. Can every sound be taken apart like "
            "this? What do you lose when you do? And is that list of partials really all there is to the difference "
            "between a flute and a violin? <bookmark mark='b'/> That is Part 3: The Spectrum."
        ) as vo:
            self.play(FadeIn(bars), FadeIn(tags))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
