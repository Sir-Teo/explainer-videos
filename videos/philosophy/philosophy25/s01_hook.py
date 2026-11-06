from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.questions()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"What then is time? \ If no one asks me, \ I know; \ if I wish to explain it to one who asks, "
                       r"\ I know not.", r"Augustine", r"\textit{Confessions} XI.14 \ (c. 400)", width=9.4,
                       font_size=27).next_to(t, DOWN, buff=0.45)
        with self.voiceover(
            "Part 24 asked why time has a direction. This part asks what space and time are in the first place. "
            "<bookmark mark='a'/>Augustine put the difficulty sixteen hundred years ago: what then is time? If no one "
            "asks me, I know; if I wish to explain it to one who asks, I know not. <bookmark mark='b'/>Physics has "
            "since given us more to explain, not less: geometries other than Euclid's, simultaneity that depends on "
            "how you move, spacetime that bends, and solutions of Einstein's equations in which you can travel into "
            "your own past. This part builds each of them, and asks what they tell us about what is real."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=TIME, scale_factor=1.03))
        self.clear_scene()

    def questions(self):
        head = label(r"Four questions", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"is space a thing?", r"a container that would exist with nothing in it \ (Newton), \ or just the "
                                   r"relations between things \ (Leibniz)?", SPACE),
            (r"is geometry a fact?", r"could we discover that space is curved, \ or do we choose a geometry by "
                                     r"convention \ (Poincaré)?", CURVE),
            (r"is the present special?", r"does only the present exist, \ or are past and future just as real, \ "
                                         r"as relativity seems to say?", LIGHT),
            (r"could the past be changed?", r"general relativity allows closed timelike curves: \ what stops the "
                                            r"time traveller?", TIME),
        ]
        g = rows_table(rows, top=1.7, gap=0.5, width=8.2, x_text=-2.0, label_size=22, text_size=21)
        with self.voiceover(
            "Four questions run through the part. <bookmark mark='a'/>Is space a thing, a container that would exist "
            "even if it held nothing, as Newton thought; or is it nothing but the relations between things, as "
            "Leibniz thought? <bookmark mark='b'/>Is the geometry of space a fact we could discover, or a convention "
            "we choose, as Poincaré argued? <bookmark mark='c'/>Is the present special: does only the present exist, "
            "or are the past and the future just as real, as relativity seems to imply? <bookmark mark='d'/>And "
            "could the past be changed? General relativity allows worlds with closed paths through time. What, then, "
            "stops the time traveller from preventing their own birth?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Newton's bucket, \ computed; \ the Leibniz--Clarke shifts, \ checked",
            r"Kant's incongruent hands, \ and the Möbius strip that turns one into the other",
            r"non-Euclidean geometry in the Poincaré disk, \ built; \ Gauss's triangle",
            r"Poincaré's disk world and conventionalism; \ spacetime structures, \ Newton to Galileo",
            r"special relativity: \ simultaneity that tilts; \ Reichenbach's $\varepsilon$ and Malament's theorem",
            r"McTaggart, \ presentism and the block; \ the Rietdijk--Putnam argument, \ computed",
            r"the hole argument \ (the Wall) \ and a Price List; \ Barbour's best matching, \ built",
            r"time travel: \ Lewis's grandfather, \ and Deutsch's fixed points, \ computed",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Newton's bucket and the arguments of Leibniz and Clarke, checked. "
            "<bookmark mark='b'/>Kant's left and right hands, and the strip that turns one into the other. "
            "<bookmark mark='c'/>Non-Euclidean geometry, built in the Poincaré disk. <bookmark mark='d'/>Poincaré's "
            "case that geometry is a convention, and the ladder of spacetime structures from Newton to Galileo. "
            "<bookmark mark='e'/>Special relativity, the relativity of simultaneity, and whether simultaneity is "
            "itself a convention. <bookmark mark='f'/>McTaggart's argument that time is unreal, the theories of "
            "time it provoked, and the argument from relativity against the present. <bookmark mark='g'/>Einstein's "
            "hole argument, this part's brick in the Wall, and a relationalist's reconstruction of dynamics. "
            "<bookmark mark='h'/>And time travel, with the paradoxes computed."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
