from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class Well(SoundScene):
    def construct(self):
        chapter(self, 5, r"Well tempered", r"Can every key be usable?", lit=(1722,), extra=((1691, r"Werckmeister's temperaments"),))
        self.recipe()
        self.compare()
        self.character()

    # ------------------------------------------------------------------
    def recipe(self):
        d = load("well")
        t = d["table"]["Werckmeister III"]
        card = history_card(1691, r"Andreas Werckmeister, \ organist at Quedlinburg",
                            r"\textit{Musicalische Temperatur}: tunings in which a player can go all the way round the circle of keys.", width=5.4, font_size=20).to_corner(UL, buff=0.4)
        circ = FifthsCircle(radius=1.9).move_to(RIGHT * 3.4 + DOWN * 0.1)
        edges = VGroup(*[circ.edge(k, color=PURE if abs(err) < 0.5 else NARROW, stroke_width=6 if abs(err) < 0.5 else 9) for k, (n, err) in enumerate(t["fifths"])])
        notes = VGroup(label(r"four fifths narrowed, \ by a quarter", font_size=26, color=NARROW), label(r"of the Pythagorean comma each:", font_size=26, color=NARROW),
                       label(r"C--G, \ G--D, \ D--A, \ and B--F$\sharp$", font_size=26, color=NARROW), label(r"the other eight: \ pure", font_size=26, color=PURE),
                       label(r"the circle closes. \ No wolf.", font_size=30, color=GOOD)).arrange(DOWN, buff=0.16, aligned_edge=LEFT).next_to(card, DOWN, buff=0.45).align_to(card, LEFT)
        with self.voiceover(
            "By the late seventeenth century composers wanted to go everywhere: to modulate through remote keys "
            "and come back. Meantone would not let them. <bookmark mark='a'/> In 1691 the organist Andreas "
            "Werckmeister published a set of tunings designed for exactly that. His third is the most famous, "
            "and it goes back to the Pythagorean comma. <bookmark mark='b'/> Take the circle of twelve pure "
            "fifths, which overshoots by one comma, and remove the comma in four equal pieces: from the fifths "
            "on C, on G, on D, and on B. <bookmark mark='c'/> The other eight fifths stay pure. The circle now "
            "closes exactly. There is no wolf anywhere."
        ) as vo:
            want = VGroup(label(r"composers wanted every key", font_size=34, color=GREY_A), label(r"meantone offered eight, \ and a wolf", font_size=30, color=BAD)).arrange(DOWN, buff=0.35).move_to(LEFT * 3.3 + DOWN * 1.0)
            self.play(FadeIn(want[0]))
            self.play(FadeIn(want[1]))
            vo.wait_until("a")
            self.play(FadeOut(want), FadeIn(card), FadeIn(circ))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(e) for e, (n, err) in zip(edges, t["fifths"]) if abs(err) > 0.5], lag_ratio=0.3), FadeIn(notes[0]), FadeIn(notes[1]), FadeIn(notes[2]), run_time=3.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(e) for e, (n, err) in zip(edges, t["fifths"]) if abs(err) < 0.5], lag_ratio=0.1), FadeIn(notes[3]), FadeIn(notes[4]), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("well")
        order = d["order"]
        head = label(r"the major third in every key: \ how many cents wider than pure", font_size=30, color=GREY_A).to_edge(UP, buff=0.35)
        panels = VGroup()
        for name, col in (("Pythagorean", None), ("meantone", None), ("Werckmeister III", None), ("equal", None)):
            vals = [v for _, v in d["table"][name]["thirds"]]
            kb = key_bars(vals, order, width=5.6, height=1.35, top=45.0, font_size=15)
            tag = label({"Pythagorean": r"Pythagorean", "meantone": r"quarter-comma meantone", "Werckmeister III": r"Werckmeister III", "equal": r"twelve equal steps"}[name],
                        font_size=24, color=TUNE).next_to(kb, UP, buff=0.18).align_to(kb, LEFT)
            panels.add(VGroup(kb, tag))
        panels.arrange_in_grid(2, 2, buff=(0.9, 0.75)).move_to(DOWN * 0.4)
        with self.voiceover(
            "What did it cost? Here is one picture for all four tunings so far: the major third in each of the "
            "twelve keys, as cents wider than pure. <bookmark mark='a'/> Pythagorean: eight thirds a comma wide, "
            "and four that happen to be nearly pure, by accident, in the keys nobody used. <bookmark mark='b'/> "
            "Meantone: eight pure thirds, and four impossible ones. <bookmark mark='c'/> Werckmeister: no third "
            "is pure, and no third is impossible. The thirds are best around C, four cents wide, and get "
            "steadily wider as you move round the circle, up to a full comma in the remote keys. "
            "<bookmark mark='d'/> And for comparison, equal temperament, which we come to next: every third the "
            "same, fourteen cents wide. Werckmeister did not remove the error. He graded it."
        ) as vo:
            self.play(FadeIn(head))
            for mark, p in zip("abcd", panels):
                vo.wait_until(mark)
                self.play(FadeIn(p[1]), FadeIn(p[0].base), FadeIn(p[0].labels), LaggedStart(*[GrowFromEdge(b, DOWN) for b in p[0].bars], lag_ratio=0.05), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def character(self):
        d = load("well")
        c = clip("well.keys")
        keys = d["keys"]
        note = listen_card(r"The major chord on C, \ on E and on F sharp, \ in Werckmeister's tuning. \\ Is it the same chord three times, \ only higher? \ Which is calmest?", width=9.6, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes([rf"{note_tex(k)} major" for k in keys], buff=0.6, width=3.0, height=1.3, font_size=30).move_to(DOWN * 0.3)
        vals = VGroup(*[label(rf"third: \ {d['wide'][k]:.0f} cents wide", font_size=26, color=error_color(d["wide"][k])).next_to(b, DOWN, buff=0.2) for k, b in zip(keys, bx)])
        with self.voiceover(
            "And that grading can be heard. Here is the major chord on C, then on E, then on F sharp, in "
            "Werckmeister's tuning. On a piano these would be the same chord at three heights. Are they here? "
            "Which is the calmest?"
        ):
            self.play(FadeIn(note, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"major chords on C, \ E and F sharp", kind="synthesized", detail=r"Werckmeister III", corner=DL, tag_corner=DR)
            for k, b in zip(keys, bx):
                t0 = snd.time_of(k)
                pulse(snd, b, t0, t0 + 2.2)
        said = VGroup(label(r"Christian Schubart, \ in the 1780s:", font_size=24, color=GREY_B),
                      label(r"C major: \ innocent, \ simple \qquad D major: \ triumph \qquad F minor: \ deep gloom", font_size=26, color=HIST),
                      label(r"eight pure fifths: \ tuned by making the beats stop", font_size=26, color=PURE)).arrange(DOWN, buff=0.18).move_to(UP * 2.2)
        card = history_card(1722, r"Johann Sebastian Bach", r"\textit{Das wohltemperirte Clavier}: a prelude and a fugue in each of the twenty-four keys. ``Well tempered'' is not ``equally tempered''.",
                            width=6.2, font_size=20).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The chord on C is calm. The one on E is brighter and more restless. The one on F sharp is tense. In a "
            "tuning like this every key has its own colour, and composers knew it: they chose a key for its "
            "character as well as for its range. Writers of the time drew up lists. For Christian Schubart, in "
            "the 1780s, C major was innocent and simple, D major was the key of triumph, and F minor the key of "
            "deep gloom. Some of that is habit and association. But some of it was in the tuning: the keys "
            "really did differ. There was a practical attraction too. Eight of Werckmeister's fifths are pure, "
            "and a pure fifth is the easiest thing in the world to tune: you simply make the beats stop. "
            "<bookmark mark='a'/> Tunings of this family are called well "
            "temperaments, and they are what the title of Bach's Well-Tempered Clavier refers to, in 1722: a "
            "prelude and a fugue in each of the twenty-four keys, to show that on a well-tempered keyboard all "
            "of them can be played. Well tempered does not mean equally tempered. On Bach's keyboard, C major "
            "and F sharp major were different places."
        ) as vo:
            self.play(FadeOut(note), FadeIn(vals))
            self.wait(8.0)
            self.play(FadeIn(said[0]), FadeIn(said[1]))
            self.wait(max(vo.until("a") - 7.0, 0.1))
            self.play(FadeIn(said[2]))
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.3)
        self.clear_scene()
