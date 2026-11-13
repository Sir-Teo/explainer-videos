from __future__ import annotations

import numpy as np

from videos.music.music7.common import *  # noqa: F403
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
        c = clip("tune.variation7")
        head = VGroup(label(r"Variation 7", font_size=48, color=TUNE),
                      label(r"one tune, \ three ways to play a string", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.4)
        lanes = lane(names=(r"plucked: \ a guitar", r"struck: \ a piano", r"bowed: \ a violin"), width=3.7, height=1.2, buff=0.4, font_size=30).move_to(UP * 0.9)
        order = ("plucked", "struck", "bowed")
        cells = VGroup()
        for k, who in enumerate(d["plan"]):
            col = VGroup(*[RoundedRectangle(width=1.3, height=0.34, corner_radius=0.08, stroke_color=GREY_D, stroke_width=1.5, fill_color=cc, fill_opacity=0.85 if nm in who else 0.0)
                           for nm, cc in zip(order, (PLUCK, STRUCK, BOWED))]).arrange(DOWN, buff=0.1)
            cells.add(VGroup(col, label(rf"phrase {k + 1}", font_size=20, color=GREY_B).next_to(col, DOWN, buff=0.12)))
        cells.arrange(RIGHT, buff=0.35).move_to(DOWN * 1.5)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built three "
            "instruments out of one string, so here they are, playing it. <bookmark mark='a'/> First each one "
            "alone: the guitar, the piano, the violin. Then the violin with each of the others. And for the "
            "last phrase, all three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lanes))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.15), run_time=2.0)
        ev = c.events
        times = [ev[f"phrase{k}"] for k in range(6)] + [ev["end"]]
        marker = SurroundingRectangle(cells[0], color=WHITE, stroke_width=2, buff=0.08).set_stroke(opacity=0)
        self.add(marker)
        with self.listen(c) as snd:
            window(snd, r"Variation 7", detail=r"a guitar, \ a piano and a violin, \ from one string", corner=DL, tag_corner=DR)
            for k, who in enumerate(d["plan"]):
                for nm in who:
                    pulse(snd, lanes[order.index(nm)], times[k], times[k + 1] - 0.05)
            snd.drive(marker, lambda m, t: m.set_stroke(opacity=1.0 if t < times[-1] else 0.0).move_to(cells[int(np.clip(np.searchsorted(times, t, side="right") - 1, 0, 5))]))
        marker.set_stroke(opacity=0)
        rws = rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.2)
        b = load("bow")
        with self.voiceover(
            f"Row seven of the ledger. {say(v['seconds'])} seconds of music, three instruments, and no recording "
            "of any of them. The measurement that goes in the ledger is the bowed string's: the force it put "
            "on the bridge matched Fourier's sawtooth, partial by partial, to within a fraction of a decibel."
        ):
            self.play(FadeOut(cells), FadeOut(marker), VGroup(lanes).animate.scale(0.6).move_to(UP * 2.1), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        t, h, s, u, b, sc = load("twomass"), load("hammer"), load("stiff"), load("unison"), load("bow"), load("schelleng")
        rows = {r["name"]: r for r in h["rows"]}
        card = objectives_card([
            r"a string moves almost no air; \ a body takes its energy, \ radiates it and filters it",
            rf"a guitar's box is a plate on a bottle: \ {t['helmholtz']:.0f} and {t['plate']:.0f} Hz alone, \ {t['lower']:.0f} and {t['upper']:.0f} Hz together",
            r"a delay and an average make a plucked string; \ the loop's length is the pitch",
            rf"felt stiffens as it is squeezed: \ a harder blow is shorter and brighter ({rows['soft']['centroid']:.0f} to {rows['hard']['centroid']:.0f} Hz)",
            rf"stiff strings stretch their partials; \ unisons a cent apart decay in two stages",
            r"a bow sticks and slips: \ a corner, \ a sawtooth, \ and a wedge of usable force",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A string by itself moves almost no air. An instrument's body takes the string's "
            "energy, radiates it, and colours it on the way. <bookmark mark='a'/> A guitar's box is a "
            "flexible plate on a bottle of air, and the two push each other's resonances apart. "
            "<bookmark mark='b'/> A plucked string is, to a computer, a delay and an average. "
            "<bookmark mark='c'/> A piano's felt stiffens as it is squeezed, so a harder blow is a shorter and "
            "brighter one. <bookmark mark='d'/> Its thick strings stretch their own partials, and its unisons, "
            "tuned a hair apart, die away in two stages. <bookmark mark='e'/> And a bow works by sticking and "
            "slipping: a corner runs round the string, the bridge feels a sawtooth, and the player's force "
            "must stay inside a wedge that narrows towards the bridge."
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
            r"A piano string has $B = 0.0004$ and a fundamental of 262 Hz. \ Find the frequencies of its 2nd, \ 4th and 8th partials, \ "
            r"and how many cents sharp each is of a whole multiple.",
            r"For a string in Helmholtz motion bowed at a fraction $\beta$ of its length from the bridge, \ show that it slips for the fraction $\beta$ of each period, \ "
            r"and that it flies back $(1-\beta)/\beta$ times as fast as the bow.",
            r"\textbf{Ear.} \ The lab plays one bowed note at five bow forces, \ in a random order. \ Put them in order of force, \ "
            r"and say which lie outside Schelleng's wedge.",
            r"\textbf{Build.} \ Add a second polarisation to \texttt{strings.pair}: \ each string can also move parallel to the soundboard, \ where the bridge hardly yields. \ "
            r"Does one string alone now decay in two stages?",
            r"$\bigstar$ \ Replace the bow's friction curve by one that depends on the rosin's temperature, \ warmed by sliding and cooled by conduction. \ "
            r"How do Schelleng's limits and the starting transient change?",
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
            (r"stick and slip with air instead of rosin: \ reeds, \ lips, \ the voice", [8]),
            (r"stiffness with no tension at all: \ bars and bells", [9]),
            (r"bowing, \ plucking and striking as colours in a score", [41]),
            (r"a delay and a filter in a loop: \ combs, \ echoes, \ reverberators", [49]),
            (r"instruments as models: \ waveguides and grids", [52]),
            (r"body resonances and where to put a microphone", [54, 56]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? In the very next part, the bow's trick of turning a steady push into a "
            "vibration returns with air in place of rosin: in reeds, in a trumpeter's lips, in the voice. The "
            "stiffness that bent the piano's partials becomes the whole story in bars and bells. The three "
            "ways of playing a string become colours for an orchestrator. Karplus and Strong's loop becomes "
            "the comb filter and the reverberator. Physical models return as a way of building synthesizers. "
            "And a body's resonances decide where a recording engineer puts the microphone."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"guitar makers", r"tap the top and listen for the air and plate resonances; \ shave the braces until they sit where the maker wants"),
            (r"piano technicians", r"needle or harden the felt to set how bright loud is; \ tune each unison by how the note dies"),
            (r"string players", r"trade bow speed, \ weight and contact point all day: \ nearer the bridge, \ slower and heavier"),
            (r"sound designers", r"reach for a plucked loop or a bowed model when a sample will not bend the way a player would"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A guitar maker taps the top, listens for the two resonances of chapter two, and "
            "shaves the braces to move them. A piano technician needles the felt to set how bright a loud note "
            "is, and tunes each unison by listening to how it dies. A string player trades speed, weight and "
            "contact point against each other all day long. And a sound designer reaches for a model, instead "
            "of a recording, when the sound has to respond the way an instrument responds to a player."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"N. H. Fletcher and T. D. Rossing, \ \textit{The Physics of Musical Instruments} \ (2nd ed., 1998)",
             r"L. Cremer, \ \textit{The Physics of the Violin} \ (1984)",
             r"A. Chaigne and J. Kergomard, \ \textit{Acoustics of Musical Instruments} \ (2016)",
             r"S. Bilbao, \ \textit{Numerical Sound Synthesis} \ (2009)"],
            [r"G. Weinreich, \ ``Coupled piano strings'', \ \textit{JASA} 62 (1977)",
             r"J. C. Schelleng, \ ``The bowed string and the player'', \ \textit{JASA} 53 (1973)",
             r"K. Karplus and A. Strong, \ ``Digital synthesis of plucked-string and drum timbres'', \ \textit{Computer Music J.} 7 (1983)",
             r"M. E. McIntyre, R. T. Schumacher and J. Woodhouse, \ ``On the oscillations of musical instruments'', \ \textit{JASA} 74 (1983)",
             r"A. Chaigne and A. Askenfelt, \ ``Numerical simulations of piano strings'', \ \textit{JASA} 95 (1994)",
             r"J. H. Smith and J. Woodhouse, \ ``The tribology of rosin'', \ \textit{J. Mech. Phys. Solids} 48 (2000)",
             r"C. Fritz et al., \ ``Soloist evaluations of six Old Italian and six new violins'', \ \textit{PNAS} 111 (2014)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        loop = VGroup(
            label(r"a steady push", font_size=30, color=GREY_A),
            label(r"something that grips, \ and lets go", font_size=30, color=BOWED),
            label(r"a resonator that says when", font_size=30, color=STR),
        ).arrange(RIGHT, buff=1.1).move_to(UP * 1.6)
        arrows = VGroup(*[Arrow(loop[i].get_right(), loop[i + 1].get_left(), color=GREY_C, buff=0.12, stroke_width=3) for i in range(2)],
                        CurvedArrow(loop[2].get_bottom() + DOWN * 0.1, loop[1].get_bottom() + DOWN * 0.1, angle=-0.9, color=GREY_C, stroke_width=3))
        rows = VGroup(label(r"bow, \ rosin, \ string", font_size=30, color=BOWED), label(r"breath, \ a reed, \ a column of air", font_size=30, color=AIR),
                      label(r"breath, \ the vocal folds, \ the throat and mouth", font_size=30, color=TUNE)).arrange(DOWN, buff=0.25).move_to(DOWN * 0.7)
        nxt = VGroup(label(r"Part 8", font_size=34, color=GREY_B), label(r"Pipes, \ Reeds and Voices", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Look once more at what the bow does, because it is the most important machine in this part. A "
            "steady push. Something that grips, and then lets go. And a resonator, the string, that sends "
            "back a signal saying when to let go next. <bookmark mark='a'/> That loop is not special to "
            "strings. Replace the bow by a player's breath, the rosin by a sliver of cane, and the string by "
            "a column of air, and you have a clarinet. <bookmark mark='b'/> Replace the cane by two folds of "
            "tissue in your throat, and you have the oldest instrument there is. <bookmark mark='c'/> Flutes, "
            "reeds, brass and the human voice: that is Part 8, Pipes, Reeds and Voices."
        ) as vo:
            self.play(LaggedStart(FadeIn(loop[0]), GrowArrow(arrows[0]), FadeIn(loop[1]), GrowArrow(arrows[1]), FadeIn(loop[2]), Create(arrows[2]), lag_ratio=0.5), run_time=6.0)
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeOut(rows), FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
