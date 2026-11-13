from __future__ import annotations

import numpy as np

from videos.music.music9.common import *  # noqa: F403
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
        c = clip("tune.variation9")
        order = d["order"]
        head = VGroup(label(r"Variation 9", font_size=48, color=TUNE),
                      label(r"one tune, \ four things that are struck", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.4)
        lanes = lane(order, [PLAYERS[n] for n in order], width=2.9, height=1.0, buff=0.25, font_size=28).move_to(UP * 1.1)
        how = [r"tuned with a knife", r"tuned on a lathe", r"tuned with a hammer", r"tuned by the air"]
        sub = VGroup(*[label(t, font_size=22, color=GREY_B).next_to(b, DOWN, buff=0.15) for t, b in zip(how, lanes)])
        cells = VGroup()
        for k, who in enumerate(d["plan"]):
            col = VGroup(*[RoundedRectangle(width=1.2, height=0.3, corner_radius=0.07, stroke_color=GREY_D, stroke_width=1.5, fill_color=PLAYERS[nm], fill_opacity=0.85 if nm in who else 0.0)
                           for nm in order]).arrange(DOWN, buff=0.08)
            cells.add(VGroup(col, label(rf"phrase {k + 1}", font_size=20, color=GREY_B).next_to(col, DOWN, buff=0.1)))
        cells.arrange(RIGHT, buff=0.35).move_to(DOWN * 1.7)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built "
            "instruments that nature tunes badly and people retuned. <bookmark mark='a'/> So here is the "
            "Tune on four of them: a marimba, bells, a steelpan and a pair of kettledrums. Each alone, "
            "then in pairs, and then together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lanes), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.15), run_time=2.0)
        ev = c.events
        times = [ev[f"phrase{k}"] for k in range(6)] + [ev["end"]]
        marker = SurroundingRectangle(cells[0], color=WHITE, stroke_width=2, buff=0.08).set_stroke(opacity=0)
        track = Line(cells.get_left() + DOWN * 1.0, cells.get_right() + DOWN * 1.0, color=GREY_D, stroke_width=2)
        runner = Dot(track.get_start(), radius=0.09, color=TUNE)
        self.add(marker, track, runner)
        with self.listen(c) as snd:
            window(snd, r"Variation 9", detail=r"computed and measured modes", corner=DL, tag_corner=DR)
            snd.drive(runner, lambda m, t: m.move_to(track.point_from_proportion(float(np.clip(t / times[-1], 0.0, 1.0)))))
            for k, who in enumerate(d["plan"]):
                for nm in who:
                    pulse(snd, lanes[order.index(nm)], times[k], times[k + 1] - 0.05)
            snd.drive(marker, lambda m, t: m.set_stroke(opacity=1.0 if t < times[-1] else 0.0).move_to(cells[int(np.clip(np.searchsorted(times, t, side="right") - 1, 0, 5))]))
            for k, nt in enumerate(c.notes):                     # every note of the Tune nudges the boxes of whoever is playing it
                snd.wait_until(f"n{k}")
                who = VGroup(*[lanes[order.index(nm)] for nm in nt["voices"]])
                self.play(who.animate(rate_func=there_and_back).scale(1.06), run_time=min(0.3, nt["dur"] * 0.6))
        marker.set_stroke(opacity=0)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]      # the ledger's last six rows
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        r = d["bar_ratios"]
        with self.voiceover(
            f"Row nine of the ledger. {say(v['seconds'])} seconds. The measurement is the knife's: every bar "
            f"of that marimba has its overtones at {say(r[1], 2)} and {say(r[2], 1)} times its note, where a "
            "plain bar would have them at two point seven six and five point four."
        ):
            self.play(FadeOut(cells), FadeOut(marker), FadeOut(track), FadeOut(runner), FadeOut(sub), lanes.animate.scale(0.6).move_to(UP * 2.2), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        t, b, bl, s = load("tabla"), load("bars"), load("bells"), load("shape")
        m = b["marimba"]
        card = objectives_card([
            r"a round skin's overtones are 1, \ 1.59, \ 2.14, \ 2.30: \ Bessel's numbers, \ and no series",
            r"air loads a kettledrum's skin towards 1 : 1.5 : 2 : 2.5; \ paste gives a tabla 1 to 5",
            rf"a bar's overtones, \ 1 : 2.76 : 5.40, \ are carved to 1 : {m['ratios'][1]:.0f} : {m['ratios'][2]:.0f} by an arch",
            rf"a bell's strike note is a missing fundamental ({bl['heard_upper_only']:.0f} Hz from 2 : 3 : 4); \ its third is minor",
            r"sand finds a plate's still lines; \ a gong's pitch follows its loudness",
            r"a spectrum gives a drum's area and rim, \ but not always its shape",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A round skin's overtones follow Bessel's numbers, and form no series. "
            "<bookmark mark='a'/> Two cultures gave a skin a note: one by letting air load it, one with a "
            "patch of paste. <bookmark mark='b'/> A bar's overtones are just as unhelpful, until an arch "
            "cut underneath moves them to two octaves and beyond. <bookmark mark='c'/> A bell's strike "
            "note is a missing fundamental, supplied by the ear, and every traditional bell carries a "
            "minor third. <bookmark mark='d'/> Sand shows where a plate stands still, and a gong's pitch "
            "is a record of its loudness. <bookmark mark='e'/> And a drum's overtones give away its area "
            "and the length of its rim, but two different shapes can share them all."
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
            r"The first zeros of the Bessel functions $J_0$, $J_1$, $J_2$ are 2.405, \ 3.832 and 5.136. \ A drumhead 60 cm across has its lowest mode at 80 Hz. \ "
            r"Find its next two modes in hertz and in cents above the lowest, \ and the speed of waves on the skin.",
            r"A bar's stiffness goes as its width times the cube of its thickness, \ and its mass per length as width times thickness. \ "
            r"Show, \ by dimensions, \ that its frequency goes as thickness over length squared, \ and that the width cancels.",
            r"\textbf{Ear.} \ The lab strikes five bells in a random order: \ some have a minor third among their partials, \ some a major third. \ "
            r"Say which is which.",
            r"\textbf{Build.} \ With \texttt{percussion.bar\_modes}, \ find a cut, \ not a simple arch, \ that puts a bar's overtones at exactly 4 and 10 times its note. \ "
            r"Where must wood come off to move the third mode alone?",
            r"$\bigstar$ \ Design a flat plate, \ by varying its thickness from place to place, \ whose five lowest modes are in the ratios 1 : 2 : 3 : 4 : 5. \ "
            r"Is there more than one answer, \ and what does Kac's question say about that?",
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
            (r"drums as the keepers of time", [11]),
            (r"scales fitted to bronze: \ the gamelan", [36]),
            (r"percussion as colour in a score", [41]),
            (r"sound from a list of dying partials", [51, 52]),
            (r"finding the blows in a recording", [61]),
            (r"a spectrum as a fingerprint", [63]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? Drums return as the keepers of time, when we reach rhythm. The "
            "bronze instruments of Java and Bali, whose overtones are not harmonic, return with scales "
            "fitted to them instead of to strings. Percussion becomes colour for an orchestrator. A list of "
            "partials, each dying at its own rate, becomes one of the cheapest ways to synthesize a sound. "
            "And the sharp start of a struck note is what a machine listens for when it transcribes music."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"timpanists", r"tune with the ear close to the head, \ and clear the skin so that every lug gives the same note"),
            (r"marimba makers", r"carve the arch in stages, \ checking the note and both overtones against a tuner after each pass"),
            (r"bell founders", r"cast a little thick, \ then turn the inside on a lathe, \ partial by partial; \ there is no putting metal back"),
            (r"sound designers", r"build every knock, \ clink and footstep in a game from a few dozen dying partials"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A timpanist tunes with an ear close to the skin, and adjusts each lug until "
            "the head gives one note all the way round. A marimba maker carves the arch in stages, checking "
            "three frequencies after each pass. A bell founder casts thick and turns metal away, knowing "
            "that none can be put back. And every knock and clink in a video game is a few dozen dying "
            "partials, computed as the objects collide."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"T. D. Rossing, \ \textit{Science of Percussion Instruments} \ (2000)",
             r"N. H. Fletcher and T. D. Rossing, \ \textit{The Physics of Musical Instruments} \ (2nd ed., 1998)",
             r"Lord Rayleigh, \ \textit{The Theory of Sound} \ (1877)",
             r"A. Lehr, \ \textit{The Art of the Carillon in the Low Countries} \ (1991)"],
            [r"C. V. Raman and S. Kumar, \ ``Musical drums with harmonic overtones'', \ \textit{Nature} 104 (1920)",
             r"T. D. Rossing, \ ``The physics of kettledrums'', \ \textit{Scientific American} 247 (1982)",
             r"M. Kac, \ ``Can one hear the shape of a drum?'', \ \textit{Amer. Math. Monthly} 73 (1966)",
             r"C. Gordon, D. Webb and S. Wolpert, \ ``One cannot hear the shape of a drum'', \ \textit{Bull. AMS} 27 (1992)",
             r"T. A. Driscoll, \ ``Eigenmodes of isospectral drums'', \ \textit{SIAM Review} 39 (1997)",
             r"T. D. Rossing and N. H. Fletcher, \ ``Nonlinear vibrations in plates and gongs'', \ \textit{JASA} 73 (1983)",
             r"A. J. G. Schoofs et al., \ ``A carillon of major-third bells'', \ \textit{Music Perception} 4 (1987)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        act = VGroup(label(r"Act I, \ Sound", font_size=40, color=TUNE),
                     label(r"a string \ $\cdot$ \ waves in air \ $\cdot$ \ the spectrum \ $\cdot$ \ the ear \ $\cdot$ \ consonance \ $\cdot$ \ tuning", font_size=26, color=GREY_A),
                     label(r"strings, \ hammers and bows \ $\cdot$ \ pipes, \ reeds and voices \ $\cdot$ \ drums, \ bars and bells", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(UP * 1.6)
        q = VGroup(label(r"we can make any sound. \ How do we tell someone else which ones, \ and when?", font_size=30, color=EAR)).move_to(DOWN * 0.5)
        nxt = VGroup(label(r"Act II, \ Notes \ $\cdot$ \ Part 10", font_size=32, color=GREY_B), label(r"Writing It Down", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "That is the end of the first act of this series. In nine parts we have gone from one string "
            "to every way an instrument makes a sound: what a vibration is, how it travels, what the ear "
            "does with it, why some sounds agree, and how strings, pipes, skins and metal are persuaded to "
            "make them. <bookmark mark='a'/> What we have not done is play anything but one small tune. To "
            "go further, music has to be remembered, and handed to someone else. Around the year 1025 a "
            "monk named Guido drew four lines across a page and boasted that a choirboy could now learn in "
            "days what used to take years. <bookmark mark='b'/> That is where Act Two begins. Part 10: "
            "Writing It Down."
        ) as vo:
            self.play(FadeIn(act[0]))
            self.play(FadeIn(act[1]), FadeIn(act[2]))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeOut(q), FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
