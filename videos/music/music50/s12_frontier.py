from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ neural models of analog gear", r"Can a network learn an amplifier?")
        self.neural()
        self.antialias()
        self.grey()
        self.problem()

    # ------------------------------------------------------------------
    def neural(self):
        items = [
            (r"record a guitar amplifier's input and output; \ train a recurrent network to map one to the other", WHITE),
            (r"Alec Wright, \ Eero-Pekka Damsk\"agg and Vesa V\"alim\"aki \ (2019--2020): \ small LSTMs that model amplifiers in real time", WHITE),
            (r"listeners struggled to tell the models from the real amplifiers in blind tests", WHITE),
            (r"commercial `capture' pedals now do this for any amplifier you own", TUNE),
            (r"the open problem: \ a model that stays right across every setting of every knob", GREY_A),
        ]
        rows_scene(self, r"amplifiers, \ learned", items,
                   "The frontier is learning the gear itself. <bookmark mark='b'/> Record a guitar amplifier's input and output, and "
                   "train a recurrent network to map one to the other. <bookmark mark='c'/> Alec Wright, Eero-Pekka Damskägg and "
                   "Vesa Välimäki showed in 2019 and 2020 that small networks can model amplifiers in real time, "
                   "<bookmark mark='d'/> and listeners struggled to tell them from the real ones in blind tests. "
                   "<bookmark mark='e'/> Commercial capture pedals now do this for any amplifier you own. <bookmark mark='f'/> The "
                   "open problem is a model that stays right across every setting of every knob.", marks="bcdef")

    # ------------------------------------------------------------------
    def antialias(self):
        items = [
            (r"oversampling works, \ but costs its factor in computation", WHITE),
            (r"antiderivative antialiasing \ (Julian Parker, \ Vadim Zavalishin and Efflam Le Bivic, \ 2016): \ shape the line between samples", WHITE),
            (r"higher orders, \ and versions for shapers with memory, \ followed \ (Stefan Bilbao and colleagues, \ 2017)", WHITE),
            (r"a network trained at a high rate can alias when run at a low one: \ the two problems meet", TUNE),
            (r"Part 51 needs the same care for oscillators", GREY_A),
        ]
        rows_scene(self, r"antialiasing nonlinearities", items,
                   "Aliasing stays a live problem. <bookmark mark='b'/> Oversampling works, but costs its factor in computation. "
                   "<bookmark mark='c'/> Antiderivative antialiasing, from Julian Parker, Vadim Zavalishin and Efflam Le Bivic in "
                   "2016, shapes the straight line between samples instead of the samples alone. <bookmark mark='d'/> Higher orders, "
                   "and versions for shapers with memory, followed, from Stefan Bilbao and colleagues. <bookmark mark='e'/> And a "
                   "network trained at one rate can alias when run at another, so the two problems meet. <bookmark mark='f'/> Part "
                   "51 needs the same care for oscillators.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take one amplifier and many settings of its knobs; \ record input and output at each", WHITE),
            (r"train one network conditioned on the knob settings", WHITE),
            (r"test it blind at settings it never saw, \ and measure its aliasing at 48 kHz", WHITE),
            (r"$\bigstar$ \ research problem: \ how small can a model be that is indistinguishable at every setting, \ and alias-free?", EAR),
            (r"an answer would say how much of an amplifier the ear can hear", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Take one amplifier and many settings of its knobs, and record "
            "input and output at each. <bookmark mark='b'/> Train one network conditioned on the knobs. <bookmark mark='c'/> "
            "Test it blind at settings it never saw, and measure its aliasing at forty-eight kilohertz. <bookmark mark='d'/> The "
            "question: how small can a model be that is indistinguishable at every setting, and free of aliasing? "
            "<bookmark mark='e'/> An answer would say how much of an amplifier the ear can hear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grey(self):
        items = [
            (r"white-box models simulate the circuit from its parts \ (Part 49's virtual analog)", WHITE),
            (r"black-box models, \ like the networks, \ learn only from input and output", WHITE),
            (r"grey-box models keep the structure, \ a filter, \ a shaper, \ a filter, \ and learn its parameters", WHITE),
            (r"differentiable shapers and compressors make that learning a gradient descent", TUNE),
            (r"the best of both: \ few parameters, \ each one meaningful, \ fitted to the real device", GREY_A),
        ]
        rows_scene(self, r"white, \ black and grey boxes", items,
                   "There is a middle way. <bookmark mark='b'/> White-box models simulate a circuit from its parts, the virtual "
                   "analogue of Part 49. <bookmark mark='c'/> Black-box models, like those networks, learn only from input and "
                   "output. <bookmark mark='d'/> Grey-box models keep the structure, a filter, a shaper and another filter, and learn "
                   "its parameters. <bookmark mark='e'/> Differentiable shapers and compressors make that learning a gradient "
                   "descent. <bookmark mark='f'/> It is the best of both: few parameters, each one meaningful, fitted to the real "
                   "device.", marks="bcdef")
