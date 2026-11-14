from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ patterns, \ machines and the scanner", r"What can be measured about improvising?")
        self.patterns()
        self.machines()
        self.scanner()
        self.problem()

    # ------------------------------------------------------------------
    def patterns(self):
        items = [
            (r"pattern mining: \ find every repeated melodic figure across hundreds of transcribed solos", WHITE),
            (r"Norgaard's analysis of Parker; \ the Weimar Jazz Database's pattern searches across players", WHITE),
            (r"results: \ some players repeat far more than others; \ figures travel between players and decades", WHITE),
            (r"open: \ is a repeated figure recalled whole, \ or rebuilt each time by the same rules?", TUNE),
            (r"Part 63 builds tools that find music by its content", GREY_A),
        ]
        rows_scene(self, r"pattern mining", items,
                   "First, pattern mining: finding every repeated melodic figure across hundreds of transcribed solos. "
                   "<bookmark mark='b'/> Martin Norgaard's analysis of Parker, and the pattern searches made on the Weimar Jazz "
                   "Database across many players, are examples. <bookmark mark='c'/> Some players repeat far more than others, "
                   "and figures travel between players and decades. <bookmark mark='d'/> An open question is whether a repeated "
                   "figure is recalled whole, or rebuilt each time by the same rules. <bookmark mark='e'/> Part 63 builds tools "
                   "that find music by its content.", marks="bcde")

    # ------------------------------------------------------------------
    def machines(self):
        items = [
            (r"John Biles's \textit{GenJam} \ (1994): \ a genetic algorithm that trades fours with its author on stage", WHITE),
            (r"Fran\c{c}ois Pachet's \textit{Continuator} \ (2003): \ learns a player's style as they play, \ and answers", WHITE),
            (r"IRCAM's \textit{OMax}: \ improvises by recombining what it has just heard", WHITE),
            (r"the best machines listen: \ the part our program leaves out", TUNE),
            (r"Part 65 returns to machines that compose", GREY_A),
        ]
        rows_scene(self, r"machine improvisers", items,
                   "Second, machine improvisers. <bookmark mark='b'/> John Biles's GenJam, from 1994, used a genetic algorithm "
                   "and traded fours with its author on stage. <bookmark mark='c'/> François Pachet's Continuator, from 2003, "
                   "learned a player's style as they played, and answered. <bookmark mark='d'/> IRCAM's OMax improvises by "
                   "recombining what it has just heard. <bookmark mark='e'/> The best of them listen, which is exactly what our "
                   "program leaves out. <bookmark mark='f'/> Part 65 returns to machines that compose.", marks="cdef")

    # ------------------------------------------------------------------
    def scanner(self):
        items = [
            (r"Charles Limb and Allen Braun \ (2008): \ jazz pianists improvising inside an MRI scanner", WHITE),
            (r"against playing memorised music: \ less activity in areas linked to self-monitoring, \ more in areas linked to self-expression", WHITE),
            (r"Donnay and colleagues \ (2014): \ trading fours with a partner in the scanner engages language areas", WHITE),
            (r"careful: \ few players, \ unusual conditions, \ and brain areas do more than one thing", TUNE),
            (r"suggestive, \ not yet explanatory", GREY_A),
        ]
        rows_scene(self, r"improvising in the scanner", items,
                   "Third, the scanner. <bookmark mark='b'/> In 2008 Charles Limb and Allen Braun had jazz pianists improvise on "
                   "a small keyboard inside an MRI scanner. <bookmark mark='c'/> Compared with playing memorised music, they "
                   "found less activity in areas linked to self-monitoring and more in areas linked to self-expression. "
                   "<bookmark mark='d'/> In 2014 Gabriel Donnay and colleagues had players trade fours with a partner, and found "
                   "language areas engaged. <bookmark mark='e'/> Careful, though: few players, unusual conditions, and brain "
                   "areas do more than one thing. <bookmark mark='f'/> Suggestive, not yet explanatory.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"collect solos with their recordings, \ transcriptions and the players' own commentary", WHITE),
            (r"model each note as recalled pattern or local choice, \ and fit the mixture per player", WHITE),
            (r"test the model's predictions against new solos, \ and against players' reports", WHITE),
            (r"$\bigstar$ \ research problem: \ how much of an improvised solo is recalled, \ and how much invented?", EAR),
            (r"an answer would turn Pressing's model into a measured one", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Collect solos with their recordings, transcriptions and the players' own "
            "commentary. <bookmark mark='b'/> Model each note as either a recalled pattern or a local choice, and fit the "
            "mixture for each player. <bookmark mark='c'/> Test the model's predictions on new solos, and against what players "
            "say they were doing. <bookmark mark='d'/> How much of an improvised solo is recalled, and how much invented? "
            "<bookmark mark='e'/> An answer would turn Pressing's model into a measured one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
