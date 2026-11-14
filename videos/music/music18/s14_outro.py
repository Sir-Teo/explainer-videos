from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403
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
        c = clip("tune.variation18")
        head = VGroup(label(r"Variation 18", font_size=48, color=TUNE), label(r"one tune, \ three basses", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        titles = {"Romanesca": r"over the Romanesca", "lament": r"in minor, \ over the chromatic lament", "pedals": r"over a tonic pedal, \ then a dominant pedal"}
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built a grammar of "
            "basses. <bookmark mark='a'/> So the Tune's two phrases are played three times, over three of them: the "
            "Romanesca, Pachelbel's falling bass, with a cadence; the chromatic lament, the Tune now in a minor "
            "key; and two pedals, the bass holding the tonic and then the dominant while the harmony changes "
            "above it. One melody, and three ways of supporting it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
        shown = None
        with self.listen(c) as snd:
            window(snd, r"Variation 18", detail=r"a plucked string", corner=DL, tag_corner=DR)
            for name in d["order"]:
                snd.wait_until(name)
                if shown is not None:
                    self.remove(*shown)
                ver = d["versions"][name]
                g = chord_roll(ver["chords"], width=10.4, height=3.0, lo=34, hi=84, thick=0.12).move_to(DOWN * 0.3)
                names = VGroup(*[label(n, font_size=22, color=TUNE) for n in ver["names"]])
                for k, n in enumerate(names):
                    n.move_to([g.xk(k), g.frame.get_bottom()[1] - 0.35, 0])
                t = label(titles[name], font_size=30, color=GREY_A).next_to(g, UP, buff=0.35)
                shown = [g, names, t]
                self.add(*shown)
                sing_chords(snd, g, ver["times_c"])
                flash(snd, list(names), ver["times_c"], hot=WHITE, base=TUNE)
        if shown is not None:
            self.remove(*shown)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row eighteen of the ledger. {say(v['seconds'])} seconds. The measurement: twenty-four chords, every "
            "one holding the Tune's note at that moment, and not one pair of voices moving in parallel fifths or "
            "octaves. The Tune is the same each time; the bass decides what it means."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        f = load("functions")["major"]
        p = load("predict")["major"]
        o = load("octave")
        card = objectives_card([
            r"chords have jobs, \ and the jobs come in an order: \ T, \ S, \ D, \ T",
            r"roots fall by fifths more than by anything else",
            rf"the next chord: \ {p['n2']:.1f} bits, \ against {p['n2_shuffled']:.1f} for the same chords shuffled",
            r"sequences, \ and new chords on strong beats",
            rf"the rule of the octave: \ Bach's chord on a stepwise bass, \ {100 * o['within']:.0f} times in a hundred",
            r"schemata: \ a vocabulary of stock phrases; \ grounds: \ one phrase, \ repeated",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Chords have jobs, and in Bach the jobs come in an order: away, tension, home. "
            "<bookmark mark='a'/> Roots fall by fifths more than they move any other way. <bookmark mark='b'/> The "
            f"next chord costs about {say(p['n2'], 1)} bits when the last one is known, a bit and a half less than "
            "if the order were random. <bookmark mark='c'/> Sequences repeat a step; new chords land on strong "
            "beats. <bookmark mark='d'/> The Neapolitans taught harmony as a rule for every note of the scale, and "
            "Bach's practice agrees with the rule about half the time. <bookmark mark='e'/> And composers of the "
            "galant style spoke in stock phrases, schemata, while for four centuries musicians have improvised "
            "over grounds, a single progression repeated."
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
            r"Write the descending-fifths sequence in G major, \ roots and bass. \ Where is the one diminished fifth, \ and why must it be there?",
            r"Show that a cycle of seven falling fifths through a major key visits every degree once, \ "
            r"and that it cannot be done with perfect fifths only.",
            r"\textbf{Ear.} \ The lab plays eight two-chord progressions. \ For each, \ say whether the root falls a fifth, \ "
            r"rises a fifth, \ or moves by step.",
            r"\textbf{Build.} \ Extend the schema detector to allow the melody notes to be ornamented \ (other notes between them). \ "
            r"How many more schemata does it find in the chorales, \ and how many in shuffled ones?",
            r"$\bigstar$ \ Design an experiment to tell whether listeners hear harmony as a chain of pairs, \ as a tree, \ "
            r"or as stock phrases.",
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
            (r"chromatic chords: \ travelling far, \ quickly", [19]),
            (r"canon and fugue", [20]),
            (r"form: \ the journey between keys", [21]),
            (r"the galant style and the classical sonata", [25, 26]),
            (r"jazz standards and the ii--V--I", [39]),
            (r"pop's four chords", [40]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? At once, in chromatic harmony, which bends this syntax to travel far. In "
            "canon and fugue, and in form, which is this syntax stretched over minutes. The galant style returns "
            "in the parts on the classical era, and the syntax of other traditions, jazz's two-five-one and pop's "
            "four chords, in parts of their own."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"keyboard players", r"learn the rule of the octave in every key: \ a chord for every bass note, \ by hand"),
            (r"songwriters", r"borrow a ground: \ the lament, \ the Romanesca, \ the four chords of pop"),
            (r"improvisers", r"think in stock phrases: \ a Prinner, \ a ii--V--I, \ a turnaround"),
            (r"arrangers", r"put new chords on strong beats, \ and let the weak beats move inside the chord"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. Keyboard players still learn the rule of the octave, as partimento teaching comes "
            "back into conservatories. Songwriters borrow grounds. Improvisers think in stock phrases, a Prinner "
            "or a two-five-one. And arrangers put new harmony on the strong beats."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"R. O. Gjerdingen, \ \textit{Music in the Galant Style} \ (2007)",
             r"G. Sanguinetti, \ \textit{The Art of Partimento} \ (2012)",
             r"F. Campion, \ \textit{Trait\'e d'accompagnement et de composition selon la r\`egle des octaves} \ (1716)",
             r"S. G. Laitz, \ \textit{The Complete Musician} \ (4th ed., \ 2015)"],
            [r"N. Mee\`us, \ ``Toward a post-Schoenbergian grammar of tonal and pre-tonal harmonic progressions'', \ \textit{Music Theory Online} 6 (2000)",
             r"M. Rohrmeier, \ ``Towards a generative syntax of tonal harmony'', \ \textit{Journal of Mathematics and Music} 5 (2011)",
             r"T. de Clercq and D. Temperley, \ ``A corpus analysis of rock harmony'', \ \textit{Popular Music} 30 (2011)",
             r"M. Neuwirth and others, \ ``The Annotated Beethoven Corpus'', \ \textit{Frontiers in Digital Humanities} 5 (2018)",
             r"R. O. Gjerdingen and J. Bourne, \ ``Schema theory as a construction grammar'', \ \textit{Music Theory Online} 21 (2015)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"how can music reach a distant key in a single chord?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"one key, \ and its neighbours", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 19", font_size=32, color=GREY_B), label(r"Chromatic Harmony", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "This part's syntax keeps to one key, and moves from it to its neighbours. <bookmark mark='a'/> But in "
            "the nineteenth century composers learned to reach distant keys in a single chord, by moving a voice "
            "or two by a semitone. How does a chord change its meaning on the way? <bookmark mark='b'/> Next time. "
            "Part 19: Chromatic Harmony."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
