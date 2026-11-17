from __future__ import annotations

import numpy as np

from videos.music.music67.common import *  # noqa: F403


class Kinds(SoundScene):
    def construct(self):
        chapter(self, 1, r"Kinds of knowing", r"What counts as evidence about music?")
        self.kinds()
        self.turns()
        self.example()
        self.questions()

    # ------------------------------------------------------------------
    def kinds(self):
        kinds = [(r"sources", r"what was written, \ by whom, \ when: \ manuscripts, \ prints, \ letters", r"Parts 23 to 27"),
                 (r"analysis", r"how a piece works: \ an argument, \ tested against the score", r"Parts 16 to 22"),
                 (r"fieldwork", r"what music means to the people who make it: \ living with them, \ recording, \ asking", r"Parts 34 to 40"),
                 (r"experiment", r"what listeners do: \ controlled conditions, \ many people, \ statistics", r"Parts 4, \ 45 to 47"),
                 (r"computation", r"what can be measured or built: \ models, \ corpora, \ benchmarks", r"Parts 61 to 66"),
                 (r"practice", r"what is learnt by making: \ composing, \ performing, \ building", r"Parts 41 to 44")]
        g = VGroup()
        for name, what, where in kinds:
            g.add(VGroup(label(name, font_size=21, color=TUNE), label(what, font_size=17, color=WHITE), label(where, font_size=15, color=GREY_A)))
        g.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.3 + LEFT * 0.2)
        for r in g:
            r[1].next_to(r[0], RIGHT, buff=0.3).align_to(g, LEFT).shift(RIGHT * 2.3)
            r[2].next_to(r[1], RIGHT, buff=0.3)
        head = label(r"six ways of knowing", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Music research knows things in at least six ways, and this series discusses all of them, while its own computations are mainly synthetic demonstrations and corpus analysis. <bookmark mark='a'/> From "
            "sources: what was written, by whom and when, from manuscripts, prints and letters. <bookmark mark='b'/> From "
            "analysis: an argument about how a piece works, tested against the score. <bookmark mark='c'/> From fieldwork: what "
            "music means to the people who make it, learnt by living with them. <bookmark mark='d'/> From experiment: what "
            "listeners do, under controlled conditions. <bookmark mark='e'/> From computation: what can be measured or built. "
            "<bookmark mark='f'/> And from practice: what is learnt by making it."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcdef", g):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def turns(self):
        items = [
            (r"Mantle Hood \ (1960): \ `bi-musicality': \ learn to perform the music you study", WHITE),
            (r"Joseph Kerman, \ \textit{Contemplating Music} \ (1985): \ musicology had become facts about sources; \ it "
             r"should be criticism too", WHITE),
            (r"Lydia Goehr, \ \textit{The Imaginary Museum of Musical Works} \ (1992): \ the fixed `work' is an idea that "
             r"settled around 1800", WHITE),
            (r"Christopher Small, \ \textit{Musicking} \ (1998): \ music is an activity, \ and everyone taking part is doing it", WHITE),
            (r"each moved what counts as evidence: \ the player's body, \ the critic's reading, \ the history of the idea, \ "
             r"the event", TUNE),
        ]
        rows_scene(self, r"how the field argued", items,
                   "The six did not arrive peacefully. <bookmark mark='b'/> In 1960 Mantle Hood asked ethnomusicologists to "
                   "learn to perform the music they study, and called it bi-musicality. <bookmark mark='c'/> In 1985 Joseph "
                   "Kerman's Contemplating Music argued that musicology had become the gathering of facts about sources, and "
                   "should be criticism as well. <bookmark mark='d'/> In 1992 the philosopher Lydia Goehr argued that the idea "
                   "of a fixed musical work, the thing a performance is of, settled into place around 1800, and is itself "
                   "historical. <bookmark mark='e'/> In 1998 Christopher Small went further: music is not a thing but an "
                   "activity, musicking, and the listeners, the dancers, even the person taking tickets at the door, are doing "
                   "it. <bookmark mark='f'/> Each of them moved what counts as evidence.", marks="bcdef")

    # ------------------------------------------------------------------
    def questions(self):
        items = [
            (r"each has its own failure: \ a misread source, \ an argument that sees what it expects, \ a field note that speaks for others", WHITE),
            (r"an experiment that does not replicate, \ a model that learnt the wrong thing, \ a practice that cannot be shared", WHITE),
            (r"and each its own check: \ collation, \ counter-example, \ consent and return, \ replication, \ held-out data, \ peer critique", WHITE),
            (r"this part takes them one at a time, \ with something to compute for each", TUNE),
        ]
        rows_scene(self, r"failures and checks", items,
                   "Each way of knowing has its own way of going wrong. <bookmark mark='b'/> A misread source; an argument that sees "
                   "what it expects; a field note that speaks for people who did not ask it to. <bookmark mark='c'/> An experiment "
                   "that does not replicate; a model that learnt the wrong thing; a practice that cannot be shared. "
                   "<bookmark mark='d'/> And each has its check: collation of sources, the counter-example, consent and the return "
                   "of recordings, replication, held-out data, and the critique of peers. <bookmark mark='e'/> This part takes them "
                   "one at a time, with something to compute for each.", marks="bcde")

    # ------------------------------------------------------------------
    def example(self):
        items = [
            (r"one question: \ where does the Tune come from?", TUNE),
            (r"sources: \ a French song, \ `Ah! \ vous dirai-je, \ maman', \ printed by 1761; \ the melody's earlier history is uncertain", WHITE),
            (r"analysis: \ its shape \ (A A$'$ B B A A$'$) \ and its harmony fit the galant style of its decade", WHITE),
            (r"fieldwork: \ how children learn it now, \ in how many languages, \ to which words", WHITE),
            (r"experiment and computation: \ how memorable it is, \ and how typical, \ against a corpus of tunes", WHITE),
            (r"practice: \ Mozart's twelve variations on it \ (Part 26), \ and this series' sixty-seven", WHITE),
        ]
        rows_scene(self, r"one question, \ six ways", items,
                   "Take one question and ask it six ways: where does the Tune come from? <bookmark mark='b'/> From sources: it is a "
                   "French song, Ah, vous dirai-je, maman, in print by 1761; its earlier history is uncertain. <bookmark mark='c'/> "
                   "From analysis: its form, a pair of phrases, a contrasting pair, and the first pair again, and its harmony fit "
                   "the galant style of that decade. <bookmark mark='d'/> From fieldwork: how children learn it now, in how many "
                   "languages and to which words. <bookmark mark='e'/> From experiment and computation: how memorable it is, and how "
                   "typical against a corpus of tunes. <bookmark mark='f'/> And from practice: Mozart's twelve variations on it, "
                   "which Part 26 measured, and this series' sixty-seven.", marks="bcdef")
