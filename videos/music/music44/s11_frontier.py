from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ scores that compose themselves", r"Can a score be written for every possible playthrough?")
        self.generative()
        self.cognition()
        self.problem()

    # ------------------------------------------------------------------
    def generative(self):
        items = [
            (r"Brian Eno's generative music for \textit{Spore} \ (2008): \ rules and samples, \ never the same twice", WHITE),
            (r"\textit{No Man's Sky} \ (2016): \ a band's recordings cut into pieces and reassembled by the game, \ endlessly", WHITE),
            (r"research systems compose to emotion targets: \ tension curves \ (Part 42) \ driven by the game's state", WHITE),
            (r"learned models now generate music to a description or to a picture \ (Parts 65 and 66)", TUNE),
            (r"the open question is control: \ the composer's intention, \ kept, \ at every moment", GREY_A),
        ]
        rows_scene(self, r"generative and adaptive scoring", items,
                   "Where is this going? <bookmark mark='b'/> Brian Eno wrote generative music for the game Spore in 2008: rules "
                   "and samples that never play the same way twice. <bookmark mark='c'/> No Man's Sky, in 2016, cut a band's "
                   "recordings into pieces and let the game reassemble them endlessly. <bookmark mark='d'/> Research systems "
                   "compose to emotion targets, tension curves like Part 42's, driven by the game's state. <bookmark mark='e'/> "
                   "Learned models now generate music to a description or a picture, Parts 65 and 66. <bookmark mark='f'/> The "
                   "open question is control: keeping the composer's intention at every moment.", marks="bcdef")

    # ------------------------------------------------------------------
    def cognition(self):
        items = [
            (r"Annabel Cohen's congruence-association model: \ music's structure is matched to the picture's, \ then its meaning attaches", WHITE),
            (r"eye tracking: \ music can steer where viewers look within a shot", WHITE),
            (r"temporal congruence: \ accents that line up with visual events bind sound and image into one", WHITE),
            (r"players play differently with different music: \ faster, \ more cautious, \ more lost", TUNE),
            (r"Part 46 asks how music makes expectation and emotion at all", GREY_A),
        ]
        rows_scene(self, r"the cognition of film and game music", items,
                   "Psychology studies how all this works. <bookmark mark='b'/> Annabel Cohen's congruence-association model: "
                   "the music's structure is first matched to the picture's, and then its meaning attaches to what matched. "
                   "<bookmark mark='c'/> Eye tracking shows music can steer where viewers look within a shot. "
                   "<bookmark mark='d'/> Accents that line up with visual events bind sound and image into one event: the hook's "
                   "lesson. <bookmark mark='e'/> And players play differently with different music: faster, more cautious, or more "
                   "lost. <bookmark mark='f'/> Part 46 asks how music makes expectation and emotion at all.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take an adaptive score with several transition rules: \ at once, \ on the bar, \ on the phrase, \ with stingers", WHITE),
            (r"have players play the same game with each, \ and measure play and enjoyment", WHITE),
            (r"also measure how often the music was `wrong': \ calm music in a fight, \ a lurch mid-phrase", WHITE),
            (r"$\bigstar$ \ research problem: \ what transition rule maximises both responsiveness and musical coherence for players?", EAR),
            (r"an answer would turn a craft rule of thumb into a measured design choice", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Take an adaptive score with several transition rules: at once, on the "
            "bar, on the phrase, with or without stingers. <bookmark mark='b'/> Have players play the same game with each, "
            "and measure how they play and how much they enjoy it. <bookmark mark='c'/> Measure how often the music was "
            "wrong: calm music in a fight, a lurch in mid-phrase. <bookmark mark='d'/> What transition rule best balances "
            "responsiveness and musical coherence for players? <bookmark mark='e'/> An answer would turn a craft rule of thumb "
            "into a measured design choice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
