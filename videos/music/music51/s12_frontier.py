from __future__ import annotations

from videos.music.music51.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ sound matching and differentiable synthesizers", r"Can a network learn to turn the knobs?")
        self.matching()
        self.differentiable()
        self.losses()
        self.problem()

    # ------------------------------------------------------------------
    def matching(self):
        items = [
            (r"make a million patches at random, \ render them, \ and train a network to map each sound back to its knobs", WHITE),
            (r"Matthew Yee-King, \ Leon Fedden and Mark d'Inverno \ (2018) \ did it for a software synthesizer, \ beating genetic search", WHITE),
            (r"InverSynth \ (Oren Barkan and others, \ 2019) \ read the knobs from a spectrogram", WHITE),
            (r"Philippe Esling's Flow Synthesizer \ (2020) \ learned a map of all presets, \ to explore by ear", WHITE),
            (r"the network learns one synthesizer: \ change the instrument and you train again", GREY_A),
        ]
        rows_scene(self, r"learning the inverse", items,
                   "The frontier replaces search with learning. <bookmark mark='b'/> Make a million patches at random, render them, "
                   "and train a network to map each sound back to the knobs that made it. <bookmark mark='c'/> Matthew Yee-King, "
                   "Leon Fedden and Mark d'Inverno did this in 2018 for a software synthesizer and beat a genetic search. "
                   "<bookmark mark='d'/> InverSynth, by Oren Barkan and colleagues in 2019, read the knobs from a spectrogram. "
                   "<bookmark mark='e'/> Philippe Esling's Flow Synthesizer of 2020 learned a map of all the presets, to be explored "
                   "by ear. <bookmark mark='f'/> But each network learns one synthesizer: change the instrument and you train "
                   "again.", marks="bcdef")

    # ------------------------------------------------------------------
    def differentiable(self):
        items = [
            (r"or make the synthesizer itself differentiable: \ every knob gets a gradient, \ and descent turns them", WHITE),
            (r"DDSP \ (Jesse Engel and others, \ 2020): \ an additive synthesizer and filtered noise inside a network", WHITE),
            (r"recursive filters are the hard part: \ gradients must flow back through every sample of feedback", WHITE),
            (r"Boris Kuznetsov, \ Julian Parker and Fabi\'an Esqueda \ (2020) \ trained IIR filters this way; \ ladders followed", WHITE),
            (r"our trapezoid-and-Newton ladder is smooth in its knobs: \ it could be differentiated, \ in principle", TUNE),
        ]
        rows_scene(self, r"differentiable synthesizers", items,
                   "The other road makes the synthesizer itself differentiable. <bookmark mark='b'/> Every knob gets a gradient, "
                   "and gradient descent turns them all at once. <bookmark mark='c'/> DDSP, by Jesse Engel and colleagues in 2020, "
                   "put an additive synthesizer and filtered noise inside a network. <bookmark mark='d'/> Recursive filters are "
                   "the hard part: gradients must flow back through every sample of feedback. <bookmark mark='e'/> Boris Kuznetsov, "
                   "Julian Parker and Fabián Esqueda trained IIR filters this way in 2020, and ladders followed. "
                   "<bookmark mark='f'/> Our trapezoid-and-Newton ladder is smooth in its knobs, so it too could be differentiated, "
                   "in principle.", marks="bcdef")

    # ------------------------------------------------------------------
    def losses(self):
        items = [
            (r"gradient descent needs a distance whose slope points the right way", WHITE),
            (r"Joseph Turian and Max Henry \ (2020): \ spectral distances are bad at pitch: \ their slope is flat or wrong away from the answer", WHITE),
            (r"so differentiable synthesizers are usually told the pitch, \ and learn only the colour", WHITE),
            (r"Ben Hayes and colleagues' review \ (2024) \ collects the methods and the open problems", WHITE),
            (r"the same knobs, \ the same distance, \ and a search that is no longer blind", TUNE),
        ]
        rows_scene(self, r"where the gradients go wrong", items,
                   "There is a catch. <bookmark mark='b'/> Gradient descent needs a distance whose slope points the right way. "
                   "<bookmark mark='c'/> Joseph Turian and Max Henry showed in 2020 that spectral distances are bad at pitch: "
                   "away from the answer their slope is flat, or wrong, as our fitting chapter warned. <bookmark mark='d'/> So "
                   "differentiable synthesizers are usually told the pitch, and learn only the colour. <bookmark mark='e'/> Ben "
                   "Hayes and colleagues' review of 2024 collects the methods and the open problems. <bookmark mark='f'/> The same "
                   "knobs, the same distance, and a search that is no longer blind.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take a two-oscillator patch with the ladder and two envelopes; \ render a thousand notes with hidden settings", WHITE),
            (r"fit each by grid search, \ by a learned inverse, \ and by descent through a differentiable ladder, \ from many starts", WHITE),
            (r"map how often descent finds the hidden settings, \ against pitch, \ resonance and the distance used", WHITE),
            (r"$\bigstar$ \ research problem: \ can gradient descent fit an analogue patch to a recorded note as reliably as a search?", EAR),
            (r"then fit notes from real analogue synthesizers, \ and judge the fits by blind listening", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Take a two-oscillator patch with the ladder and two envelopes, "
            "and render a thousand notes with hidden settings. <bookmark mark='b'/> Fit each by grid search, by a learned "
            "inverse, and by descent through a differentiable ladder from many starting points. <bookmark mark='c'/> Map how "
            "often descent finds the hidden settings, against pitch, resonance and the distance used. <bookmark mark='d'/> The "
            "question: can gradient descent fit an analogue patch to a recorded note as reliably as a search? "
            "<bookmark mark='e'/> Then fit notes from real analogue synthesizers, and judge the fits by blind listening."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
