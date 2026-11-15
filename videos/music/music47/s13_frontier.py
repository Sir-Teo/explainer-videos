from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ data at the scale of the species", r"What would settle the questions?")
        self.datasets()
        self.genes()
        self.open_()
        self.problem()

    # ------------------------------------------------------------------
    def datasets(self):
        items = [
            (r"the Global Jukebox \ (2022): \ Alan Lomax's coded song recordings, \ about 5,800 songs from about 1,000 societies", WHITE),
            (r"the Natural History of Song: \ open ethnographies and recordings, \ with the code to analyse them", WHITE),
            (r"many-site studies like Jacoby's and Ozaki's: \ the same experiment, \ run by researchers in dozens of places", WHITE),
            (r"Registered Reports: \ hypotheses fixed before the data, \ so that a null result is published too", TUNE),
            (r"the old weakness was samples of one culture; \ the new risk is coding the world in one culture's categories", GREY_A),
        ]
        rows_scene(self, r"datasets of the world's music", items,
                   "The frontier is data at the scale of the species. <bookmark mark='b'/> The Global Jukebox, published in "
                   "2022, makes Alan Lomax's coded recordings public: about fifty-eight hundred songs from about a thousand "
                   "societies. <bookmark mark='c'/> The Natural History of Song is open too, with the code to analyse it. "
                   "<bookmark mark='d'/> Studies like Jacoby's and Ozaki's run the same experiment with researchers in dozens of "
                   "places. <bookmark mark='e'/> And Registered Reports fix the hypotheses before the data, so that a null "
                   "result is published too. <bookmark mark='f'/> The old weakness was samples from one culture; the new risk "
                   "is coding the world's music in one culture's categories.", marks="bcdef")

    # ------------------------------------------------------------------
    def genes(self):
        items = [
            (r"Maria Niarchou and colleagues \ (2022): \ 606,825 people asked `can you clap in time with a musical beat?'", WHITE),
            (r"the answer was checked against measured tapping in separate experiments", WHITE),
            (r"69 places in the genome were linked to it; \ together, \ common variants explain 13 to 16 per cent", WHITE),
            (r"genes active in the brain, \ and links to breathing, \ motor function, \ processing speed and sleep timing", TUNE),
            (r"highly polygenic: \ no gene for rhythm, \ but thousands of small nudges, \ and much left to environment", GREY_A),
        ]
        rows_scene(self, r"the genetics of rhythm", items,
                   "Genetics has arrived too. <bookmark mark='b'/> In 2022 Maria Niarchou and colleagues analysed 606,825 people "
                   "who had answered one question: can you clap in time with a musical beat? <bookmark mark='c'/> The answer "
                   "was checked against measured tapping in separate experiments. <bookmark mark='d'/> Sixty-nine places in "
                   "the genome were linked to it, and common variants together explained thirteen to sixteen per cent of the "
                   "differences. <bookmark mark='e'/> The genes are active in the brain, with links to breathing, motor "
                   "function, processing speed and the timing of sleep. <bookmark mark='f'/> It is highly polygenic: no gene "
                   "for rhythm, but thousands of small nudges, and much left to experience.", marks="bcdef")

    # ------------------------------------------------------------------
    def open_(self):
        items = [
            (r"is the beat a human specialization, \ or a vocal learner's, \ or a mammal's?", WHITE),
            (r"which universals come from perception, \ which from memory, \ which from transmission?", WHITE),
            (r"do small-integer rhythm priors appear before any musical experience?", WHITE),
            (r"what did music do for the people who carved the first flutes?", TUNE),
            (r"answers need the same experiment everywhere, \ and models that say what each answer predicts", GREY_A),
        ]
        rows_scene(self, r"open questions", items,
                   "Some open questions. <bookmark mark='b'/> Is the beat a human specialization, a vocal learner's, or a "
                   "mammal's? <bookmark mark='c'/> Which universals come from perception, which from memory, and which from "
                   "transmission? <bookmark mark='d'/> Do small-integer rhythm priors appear before any musical experience? "
                   "<bookmark mark='e'/> And what did music do for the people who carved the first flutes? "
                   "<bookmark mark='f'/> Answers need the same experiment everywhere, and models that say what each answer "
                   "predicts.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"run simulated transmission chains with each bias switched off in turn: \ noise, \ categories, \ memory, \ the leap cost", WHITE),
            (r"for each, \ measure which of Savage's universals still emerge, \ and how fast", WHITE),
            (r"then fit the biases to real transmission chains, \ in the lab or in tune families", WHITE),
            (r"$\bigstar$ \ research problem: \ which universals need which biases, \ and are those biases themselves universal?", EAR),
            (r"an answer would separate what the mind supplies from what history adds", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Run simulated transmission chains with each bias switched "
            "off in turn: the noise, the categories, the memory, the cost of leaps. <bookmark mark='b'/> For each, measure "
            "which of Savage's universals still emerge, and how fast. <bookmark mark='c'/> Then fit the biases to real "
            "transmission chains, in the lab or in tune families. <bookmark mark='d'/> The question: which universals need "
            "which biases, and are those biases themselves universal? <bookmark mark='e'/> An answer would separate what the "
            "mind supplies from what history adds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
