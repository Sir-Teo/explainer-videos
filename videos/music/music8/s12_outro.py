from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403
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
        c = clip("tune.variation8")
        order = d["order"]
        head = VGroup(label(r"Variation 8", font_size=48, color=TUNE),
                      label(r"one tune, \ five columns of air", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.4)
        lanes = lane(order, [PLAYERS[n] for n in order], width=2.35, height=1.0, buff=0.2, font_size=28).move_to(UP * 1.1)
        valves = [r"a jet", r"a reed", r"a reed, \ a cone", r"lips", r"vocal folds"]
        sub = VGroup(*[label(t, font_size=22, color=GREY_B).next_to(b, DOWN, buff=0.15) for t, b in zip(valves, lanes)])
        cells = VGroup()
        for k, who in enumerate(d["plan"]):
            col = VGroup(*[RoundedRectangle(width=1.2, height=0.26, corner_radius=0.07, stroke_color=GREY_D, stroke_width=1.5, fill_color=PLAYERS[nm], fill_opacity=0.85 if nm in who else 0.0)
                           for nm in order]).arrange(DOWN, buff=0.07)
            cells.add(VGroup(col, label(rf"phrase {k + 1}", font_size=20, color=GREY_B).next_to(col, DOWN, buff=0.1)))
        cells.arrange(RIGHT, buff=0.35).move_to(DOWN * 1.7)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built five "
            "instruments, each a valve on a column of air: a jet, a reed on a cylinder, a reed on a cone, a "
            "pair of lips, and the vocal folds. <bookmark mark='a'/> Here they are, a phrase each, and then "
            "all five together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lanes), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.15), run_time=2.0)
        ev = c.events
        times = [ev[f"phrase{k}"] for k in range(6)] + [ev["end"]]
        marker = SurroundingRectangle(cells[0], color=WHITE, stroke_width=2, buff=0.08).set_stroke(opacity=0)
        self.add(marker)
        with self.listen(c) as snd:
            window(snd, r"Variation 8", detail=r"five model instruments", corner=DL, tag_corner=DR)
            for k, who in enumerate(d["plan"]):
                for nm in who:
                    pulse(snd, lanes[order.index(nm)], times[k], times[k + 1] - 0.05)
            snd.drive(marker, lambda m, t: m.set_stroke(opacity=1.0 if t < times[-1] else 0.0).move_to(cells[int(np.clip(np.searchsorted(times, t, side="right") - 1, 0, 5))]))
        marker.set_stroke(opacity=0)
        rws = rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            f"Row eight of the ledger. {say(v['seconds'])} seconds. Each wind instrument was tuned the way a "
            "maker tunes one: built, blown, measured and trimmed, until every note was within "
            f"{say(max(np.ceil(d['worst_cents']), 1))} cents of its pitch."
        ):
            self.play(FadeOut(cells), FadeOut(marker), FadeOut(sub), lanes.animate.scale(0.55).move_to(UP * 2.35), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        h, r, o, k, l, s = load("hook"), load("reed"), load("holes"), load("cone"), load("lips"), load("singers")
        card = objectives_card([
            r"open at both ends, \ a pipe has every harmonic; \ closed at one, \ only the odd ones",
            rf"a reed feeds the pipe only above a third of its closing pressure ({r['threshold']:.2f} here)",
            rf"holes shorten the pipe; \ a register hole gives the next resonance: \ an octave, \ or a twelfth",
            rf"a cone has every harmonic; \ a bell and mouthpiece turn 1, 3, 5 into 2, 3, 4, 5 \ ({l['f0']:.0f} Hz)",
            r"a flute's jet must take half a period to cross; \ blown harder, \ it finds the octave",
            rf"a voice is a source and a filter: \ formants make vowels, \ ring (+{s['boost_db']:.0f} dB), \ and overtones",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A pipe open at both ends has every harmonic. Closed at one end, it sounds an "
            "octave lower and has only the odd ones. <bookmark mark='a'/> A reed is a valve that the pressure "
            "closes, and it feeds the pipe only above a third of the pressure that shuts it. "
            "<bookmark mark='b'/> Holes shorten the pipe, and a register hole hands the note to the next "
            "resonance: an octave up for a flute or an oboe, a twelfth for a clarinet. <bookmark mark='c'/> A "
            "cone has every harmonic, and a brass instrument's bell and mouthpiece bend an odd series into "
            "a whole one. <bookmark mark='d'/> A flute is played by a jet whose crossing takes half a period, "
            "so that blowing harder finds the octave. <bookmark mark='e'/> And a voice is a source and a "
            "filter, with the pitch in one and the vowel in the other: until a singer moves the filter on "
            "purpose, for power or for a second note."
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
            r"A pipe is 40 cm long and 2 cm wide. \ Find its three lowest resonances when it is open at both ends, \ and when it is closed at one, \ "
            r"with and without the end correction of 0.61 of the radius for each open end.",
            r"The flow through a reed is $u = \zeta\,(1 - \Delta)\sqrt{\Delta}$, \ where $\Delta$ is the pressure across it as a fraction of the closing pressure. \ "
            r"Show that $u$ is greatest at $\Delta = \tfrac13$, \ and explain why a clarinet cannot speak below it.",
            r"\textbf{Ear.} \ The lab sings one note on four vowels, \ in a random order. \ Name the four words, \ "
            r"and say which formant told you each.",
            r"\textbf{Build.} \ With \texttt{winds.Bore}, \ put six holes of 4 mm radius in the 60 cm clarinet so that opening them in turn gives a major scale. \ "
            r"How far are they from where a saw would cut?",
            r"$\bigstar$ \ Give the reed a second tube, \ upstream: \ the player's vocal tract. \ When does a resonance of the tract capture the note, \ "
            r"and can the model bend a clarinet's pitch the way players do?",
        ], font_size=23)
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
            (r"more things that vibrate, \ and are not harmonic at all", [9]),
            (r"the colours of the winds, \ for an orchestrator", [41]),
            (r"adding partials, \ and filtering a rich source", [51]),
            (r"instruments as loops of delay", [52]),
            (r"a source and a filter, \ for sending speech down a wire", [58]),
            (r"the voice as the first instrument", [47]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? Next, in instruments whose overtones are not harmonic at all. The "
            "colours of flute, reed and brass become an orchestrator's palette. The organ's stops and the "
            "voice's filter become the two oldest ways of building a synthesizer: add partials, or carve "
            "them from a rich source. The loop of delay returns as a way to model anything. The source and "
            "the filter become the trick by which a telephone sends a voice in a few thousand numbers a "
            "second. And the voice returns when we ask where music came from."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"woodwind makers", r"place and size each hole against a computed impedance, \ then undercut it by hand until the registers agree"),
            (r"brass players", r"buzz the lips to a note before the horn confirms it; \ practise the pedal to learn the feel of each resonance"),
            (r"singers and their teachers", r"lower the larynx for ring; \ open the vowel as the pitch rises; \ choose words for high notes with care"),
            (r"speech engineers", r"separate every voice into a pitch and a filter, \ and send, \ store or change each one alone"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A woodwind maker places each hole against a computed curve, and then "
            "undercuts it by hand until the registers agree. A brass player learns to buzz the note before "
            "the horn confirms it. A singing teacher asks for a lower larynx and a more open vowel as the "
            "pitch rises, and a good librettist does not put an ee on a soprano's high note. And a speech "
            "engineer splits every voice into a pitch and a filter, and sends, stores or changes each one "
            "alone."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"A. H. Benade, \ \textit{Fundamentals of Musical Acoustics} \ (1976)",
             r"N. H. Fletcher and T. D. Rossing, \ \textit{The Physics of Musical Instruments} \ (2nd ed., 1998)",
             r"A. Chaigne and J. Kergomard, \ \textit{Acoustics of Musical Instruments} \ (2016)",
             r"J. Sundberg, \ \textit{The Science of the Singing Voice} \ (1987)"],
            [r"J. Backus, \ ``Small-vibration theory of the clarinet'', \ \textit{JASA} 35 (1963)",
             r"J. W. Coltman, \ ``Sounding mechanism of the flute and organ pipe'', \ \textit{JASA} 44 (1968)",
             r"M. E. McIntyre, R. T. Schumacher and J. Woodhouse, \ ``On the oscillations of musical instruments'', \ \textit{JASA} 74 (1983)",
             r"G. E. Peterson and H. L. Barney, \ ``Control methods used in a study of the vowels'', \ \textit{JASA} 24 (1952)",
             r"J. Sundberg, \ ``Articulatory interpretation of the `singing formant'\,'', \ \textit{JASA} 55 (1974)",
             r"E. Joliveau, J. Smith and J. Wolfe, \ ``Tuning of vocal tract resonance by sopranos'', \ \textit{Nature} 427 (2004)",
             r"C. Bergevin et al., \ ``Overtone focusing in biphonic Tuvan throat singing'', \ \textit{eLife} 9 (2020)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        left = VGroup(label(r"a string, \ a column of air", font_size=30, color=AIR), label(r"long and thin: \ one dimension", font_size=24, color=GREY_A),
                      MathTex(r"f,\ 2f,\ 3f,\ 4f \ldots", font_size=38, color=AIR)).arrange(DOWN, buff=0.2).move_to(LEFT * 3.5 + UP * 1.0)
        right = VGroup(label(r"a drumhead, \ a bar, \ a bell", font_size=30, color=BRASS), label(r"wide, \ or stiff, \ or both", font_size=24, color=GREY_A),
                       MathTex(r"f,\ 1.59f,\ 2.14f,\ 2.30f \ldots", font_size=38, color=BRASS)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.5 + UP * 1.0)
        q = label(r"if the overtones are not harmonics, \ what is the note?", font_size=32, color=EAR).move_to(DOWN * 1.0)
        nxt = VGroup(label(r"Part 9", font_size=34, color=GREY_B), label(r"Drums, \ Bars and Bells", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Everything we have built so far, in this part and the last, has had one thing in common. A "
            "string and a column of air are long and thin, and a long thin thing has overtones that are "
            "whole multiples of its fundamental, or close to it. That is why they have a clear pitch, and "
            "why Parts 5 and 6 could build consonance and tuning on them. <bookmark mark='a'/> But hit a "
            "drum. Its overtones are at one point five nine, two point one four, two point three times the "
            "fundamental: nothing like a harmonic series. A xylophone bar is worse, and a bell is worse "
            "still. <bookmark mark='b'/> So what note is a bell playing? And how did makers, long before "
            "anyone could compute it, persuade bars and bells to play in tune? That is Part 9: Drums, Bars "
            "and Bells."
        ) as vo:
            self.play(FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(right))
            vo.wait_until("b")
            self.play(FadeIn(q))
            self.wait(max(vo.remaining() - 4.5, 0.1))
            self.play(FadeOut(q), FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
