from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ sixty years of charts", r"What can a corpus of hits tell us?")
        self.mauch()
        self.serra()
        self.platforms()
        self.missing()
        self.problem()

    # ------------------------------------------------------------------
    def mauch(self):
        items = [
            (r"Matthias Mauch and colleagues \ (2015): \ about 17,000 songs from the US Hot 100, \ 1960--2010", WHITE),
            (r"audio analysed for chord types and timbre, \ by machine", WHITE),
            (r"change came in bursts, \ `revolutions', \ around 1964, \ 1983 and 1991", WHITE),
            (r"1991: \ the rise of hip hop, \ with fewer chord changes and more rhythm and timbre", TUNE),
            (r"Part 62 builds the chord and beat trackers such studies need", GREY_A),
        ]
        rows_scene(self, r"the evolution of popular music", items,
                   "In 2015 Matthias Mauch and colleagues analysed about seventeen thousand songs from the American Hot 100, from "
                   "1960 to 2010. <bookmark mark='b'/> They analysed the audio itself, by machine, for chord types and timbre. "
                   "<bookmark mark='c'/> Change came in bursts, which they called revolutions, around 1964, 1983 and 1991. "
                   "<bookmark mark='d'/> The largest, in 1991, came with the rise of hip hop: fewer chord changes, more rhythm and "
                   "timbre. <bookmark mark='e'/> Part 62 builds the chord and beat trackers such studies need.", marks="bcde")

    # ------------------------------------------------------------------
    def serra(self):
        items = [
            (r"Joan Serr\`a and colleagues \ (2012): \ the Million Song Dataset, \ 1955--2010", WHITE),
            (r"they reported narrower pitch transitions, \ more homogeneous timbre, \ and rising loudness over time", WHITE),
            (r"Hubert L\'eveill\'e Gauvin \ (2018): \ shorter intros, \ earlier voices and titles", WHITE),
            (r"caution: \ charts reflect sales, \ marketing and the measuring method, \ not only taste", TUNE),
            (r"a corpus shows what changed; \ explaining why needs history and experiment", GREY_A),
        ]
        rows_scene(self, r"more corpora", items,
                   "Others agree in part. <bookmark mark='b'/> Joan Serrà and colleagues, in 2012, analysed the Million Song "
                   "Dataset from 1955 to 2010, <bookmark mark='c'/> and reported narrower pitch transitions, more homogeneous "
                   "timbre, and rising loudness over time. <bookmark mark='d'/> Hubert Léveillé Gauvin's shorter intros, earlier "
                   "voices and earlier titles fit the same story. <bookmark mark='e'/> But caution: charts reflect sales, marketing "
                   "and the way they are measured, not only taste. <bookmark mark='f'/> A corpus shows what changed; explaining "
                   "why needs history and experiment.", marks="cdef")

    # ------------------------------------------------------------------
    def platforms(self):
        items = [
            (r"several chart analyses report that hit songs have grown shorter since the 1990s", WHITE),
            (r"some services count streams after thirty seconds; \ short-video excerpts vary", WHITE),
            (r"songs are now written so that one moment can be cut out and travel on its own", WHITE),
            (r"whether the platforms cause the change, \ or only accelerate it, \ is open", TUNE),
            (r"the medium shapes the form: \ Part 21's lesson, \ for the twenty-first century", GREY_A),
        ]
        rows_scene(self, r"platforms", items,
                   "The newest change is still under way. <bookmark mark='b'/> Several chart analyses report that hit songs have grown shorter since the 1990s. <bookmark mark='c'/> Some streaming services count plays after thirty seconds, with varied payment arrangements, and short-video platforms circulate excerpts of varying length, <bookmark mark='d'/> which can reward an excerpt that travels independently; establishing a general causal effect on songwriting requires more evidence. <bookmark mark='e'/> Whether the platforms cause the change, or only accelerate it, is open. <bookmark mark='f'/> The medium shapes the form: Part 21's lesson, for the twenty-first century.", marks="cdef")

    # ------------------------------------------------------------------
    def missing(self):
        items = [
            (r"most corpus studies use the US or UK charts: \ English-language, \ commercial, \ recorded", WHITE),
            (r"global streaming charts now mix Latin, \ K-pop, \ Afrobeats and Indian film music", WHITE),
            (r"a theory of `the song' built on one country's charts describes that country", WHITE),
            (r"Act VI's lesson: \ measure each music in its own terms", TUNE),
            (r"Part 47 asks what is shared across all of them", GREY_A),
        ]
        rows_scene(self, r"what the charts leave out", items,
                   "And what do the charts leave out? <bookmark mark='b'/> Most corpus studies use the American or British "
                   "charts: English-language, commercial, recorded music. <bookmark mark='c'/> Global streaming charts now mix "
                   "Latin pop, K-pop, Afrobeats and Indian film music. <bookmark mark='d'/> A theory of the song built on one "
                   "country's charts describes that country. <bookmark mark='e'/> Act Six's lesson applies: measure each music "
                   "in its own terms. <bookmark mark='f'/> Part 47 asks what is shared across all of them.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"build a corpus of hits with release dates, \ platform histories and audio", WHITE),
            (r"measure intro length, \ time to the hook, \ song length and repetition, \ year by year", WHITE),
            (r"compare songs that spread on short-video platforms with those that did not, \ before and after", WHITE),
            (r"$\bigstar$ \ research problem: \ do new platforms change how songs are written, \ or only which songs win?", EAR),
            (r"the answer separates the composer's choice from the market's selection", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Build a corpus of hits with release dates, platform histories and "
            "audio. <bookmark mark='b'/> Measure intro length, time to the hook, song length and repetition, year by year. "
            "<bookmark mark='c'/> Compare songs that spread on short-video platforms with those that did not, before and "
            "after. <bookmark mark='d'/> Do new platforms change how songs are written, or only which songs win? "
            "<bookmark mark='e'/> The answer separates the composer's choice from the market's selection."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
