from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403


class Print(SoundScene):
    def construct(self):
        chapter(self, 6, r"Printing, and Josquin's name", r"What happens to a composer's name when music is sold?", extra=((1501, r"Petrucci's \textit{Odhecaton}"),))
        self.petrucci()
        self.josquin()
        self.evidence()

    # ------------------------------------------------------------------
    def petrucci(self):
        items = [
            (r"1501, \ Venice: \ Ottaviano Petrucci prints the \textit{Harmonice musices odhecaton}", WHITE),
            (r"96 songs, \ mostly French chansons, \ each page printed in three impressions", WHITE),
            (r"soon: \ books of Masses by single composers, \ the first by Josquin \ (1502)", WHITE),
            (r"a name on a title page sells copies: \ the composer as a brand", TUNE),
            (r"and a name in a print travels further than the manuscript it came from", GREY_A),
        ]
        rows_scene(self, r"music printed", items,
                   "In 1501, in Venice, Ottaviano Petrucci printed a book of polyphonic music from movable type, the "
                   "Harmonice musices odhecaton, the hundred songs of its title, ninety-six in fact. <bookmark mark='b'/> Most "
                   "were French chansons, and "
                   "each page went through the press three times, for the staves, the notes and the words. "
                   "<bookmark mark='c'/> A year later he printed a book of Masses all by one composer, and the composer "
                   "was Josquin. <bookmark mark='d'/> A name on a title page sells copies, and Josquin's name became a "
                   "brand. <bookmark mark='e'/> A name in a print also travels much further than the manuscript a "
                   "printer copied from, with whatever mistakes that manuscript held.")

    # ------------------------------------------------------------------
    def josquin(self):
        items = [
            (r"Josquin des Prez, \ about 1450--1521: \ Milan, \ Rome, \ Ferrara, \ Condé", WHITE),
            (r"praised by Luther: \ `the master of the notes; \ they must do as he wills'", WHITE),
            (r"after his death, \ prints in Germany add works under his name", WHITE),
            (r"some had other names in earlier sources; \ some were by younger composers", EAR),
            (r"modern scholarship has shrunk the list: \ the famous motets are not all safe", GREY_A),
        ]
        rows_scene(self, r"a famous name", items,
                   "Josquin worked in Milan, in the papal chapel in Rome, at the court of Ferrara, and ended his life at "
                   "Condé in the north of France. <bookmark mark='b'/> He was admired as no composer before him: Martin "
                   "Luther said that Josquin was the master of the notes, which must do as he wills, while other "
                   "composers must do as the notes will. <bookmark mark='c'/> After his death, German printers in "
                   "particular published more and more under his name. <bookmark mark='d'/> Some of those pieces carry "
                   "other composers' names in earlier sources; some are in the style of a younger generation. "
                   "<bookmark mark='e'/> Modern scholars have shrunk the list, and some once-famous motets are no longer "
                   "thought to be his. How do you decide?")

    # ------------------------------------------------------------------
    def evidence(self):
        cols = VGroup()
        for t, items, col in ((r"the sources", [r"how early, \ how close to him", r"conflicting names", r"which scribe, \ which printer"], BLUE),
                              (r"the style", [r"dissonance, \ cadences, \ textures", r"how the voices are laid out", r"habits too small to imitate"], TUNE)):
            box = RoundedRectangle(width=5.4, height=3.0, corner_radius=0.15, stroke_color=col, stroke_width=2)
            g = VGroup(label(t, font_size=28, color=col), *[label(x, font_size=21, color=WHITE) for x in items]).arrange(DOWN, buff=0.28).move_to(box)
            cols.add(VGroup(box, g))
        cols.arrange(RIGHT, buff=0.8).move_to(UP * 0.2)
        cap = label(r"style evidence is the circular kind: \ the `secure' works define the style that judges the rest", font_size=22, color=EAR).to_edge(DOWN, buff=0.55)
        head = label(r"two kinds of evidence", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "There are two kinds of evidence. <bookmark mark='a'/> The sources: how early a copy is, how close to the "
            "composer, whether other sources give another name, which scribe or printer made it. "
            "<bookmark mark='b'/> And the style: how a piece treats dissonance, cadences, texture, and the small habits "
            "a composer has without thinking, which an imitator would not copy. <bookmark mark='c'/> Style evidence has a "
            "danger built in: the works we are sure of define the style that is then used to judge the rest, so a "
            "mistaken attribution can teach the test the wrong style. The next chapter builds such a test, and asks what "
            "it can and cannot show."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
