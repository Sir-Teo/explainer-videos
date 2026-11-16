from __future__ import annotations

from videos.music.music52.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ neural and differentiable physical models", r"Can a model be learned from a recording?")
        self.learned()
        self.hybrids()
        self.problem()

    # ------------------------------------------------------------------
    def learned(self):
        items = [
            (r"make each method differentiable, \ then fit it to recordings by gradient descent \ (Part 51's frontier)", WHITE),
            (r"DDX7 \ (Franco Caspe, \ Andrew McPherson and Mark Sandler, \ 2022): \ a network that plays a DX7-style FM engine to imitate real instruments", WHITE),
            (r"differentiable modal resonators \ (Rodrigo Diaz and colleagues, \ 2023): \ an object's modes learned from its shape", WHITE),
            (r"DDSP-Piano \ (Lenny Renault, \ R\'emi Mignot and Axel Roebel): \ inharmonic partials and a residual, \ fitted to a real piano", WHITE),
            (r"each keeps the synthesizer's structure, \ so its knobs still mean something", TUNE),
        ]
        rows_scene(self, r"methods that learn", items,
                   "Every method of this part is now being learned. <bookmark mark='b'/> Make it differentiable, as Part 51's "
                   "frontier described, then fit it to recordings by gradient descent. <bookmark mark='c'/> DDX7, from Franco "
                   "Caspe, Andrew McPherson and Mark Sandler in 2022, is a network that plays a DX7-style FM engine to imitate real "
                   "instruments. <bookmark mark='d'/> Rodrigo Diaz and colleagues in 2023 learned an object's modes from its shape. "
                   "<bookmark mark='e'/> DDSP-Piano, from Lenny Renault, Rémi Mignot and Axel Roebel, fits inharmonic partials and a "
                   "residual to a real piano, much as our spectral chapter did. <bookmark mark='f'/> Each keeps the synthesizer's "
                   "structure, so its knobs still mean something.", marks="bcdef")

    # ------------------------------------------------------------------
    def hybrids(self):
        items = [
            (r"black boxes: \ a network maps controls straight to sound; \ realistic, \ but nothing inside to turn \ (Part 66)", WHITE),
            (r"grey boxes: \ a physical or FM core with learned parts, \ such as a reed's curve or a body's resonances", WHITE),
            (r"the test is the hard one: \ does the model react correctly to playing it never saw, \ like a sampler cannot?", WHITE),
            (r"Part 7's string and this part's clarinet are white boxes: \ every number is physics", WHITE),
            (r"the frontier runs between them", TUNE),
        ]
        rows_scene(self, r"black, \ grey and white", items,
                   "There is a spectrum of models. <bookmark mark='b'/> Black boxes: a network maps controls to sound; internal features are less directly tied to physical parameters, though controls and realism vary, Part 66's subject. <bookmark mark='c'/> Grey boxes: a physical or FM core with learned parts, such as a reed's curve or a body's resonances. <bookmark mark='d'/> The test is the hard one: does the model react correctly to playing it never saw, beyond the training recordings? <bookmark mark='e'/> Part 7's string and this part's clarinet are white-box models with explicit equations and simplifying assumptions. <bookmark mark='f'/> The frontier runs between them.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"record an instrument across its range and dynamics; \ hold out some notes and playing styles", WHITE),
            (r"fit a sampler, \ a differentiable FM engine, \ a modal model and a waveguide to the rest", WHITE),
            (r"compare them on the held-out playing, \ by blind listening, \ against their size in bytes", WHITE),
            (r"$\bigstar$ \ research problem: \ how few parameters can match an instrument across its range, \ including playing it never heard?", EAR),
            (r"an answer would rank the methods of this part by what they really know", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Record an instrument across its range and dynamics, and hold "
            "out some notes and playing styles. <bookmark mark='b'/> Fit a sampler, a differentiable FM engine, a modal model and "
            "a waveguide to the rest. <bookmark mark='c'/> Compare them on the held-out playing, by blind listening, against "
            "their size in bytes. <bookmark mark='d'/> The question: how few parameters can match an instrument across its "
            "range, including playing it never heard? <bookmark mark='e'/> An answer would rank this part's methods by what "
            "they really know."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
