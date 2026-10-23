from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (ATT, CNN, HIST, KERNEL, LSTMC, PART, grid_of, img_filter, img_heat, img_rgb, load)


class Hook(VoiceoverScene):
    def construct(self):
        self.cat()
        self.ours()
        self.remember()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def cat(self):
        hc = history_card(1959, r"David Hubel \& Torsten Wiesel", r"single neurons in a cat's visual cortex",
                          width=5.4, color=HIST).to_corner(UL, buff=0.4)
        screen = Rectangle(width=4.2, height=3.0, stroke_color=GREY_B, stroke_width=2, fill_color="#0B0F17",
                           fill_opacity=1).move_to([-3.4, -0.9, 0])
        sl = label(r"the screen the cat looks at", font_size=20, color=GREY_B).next_to(screen, DOWN, buff=0.12)
        x = ValueTracker(-2.0)

        def edge():
            xx = x.get_value()
            lit = Polygon(screen.get_corner(UL), [screen.get_left()[0] + 2.1 + xx + 0.6, screen.get_top()[1], 0],
                          [screen.get_left()[0] + 2.1 + xx - 0.6, screen.get_bottom()[1], 0], screen.get_corner(DL),
                          stroke_width=0, fill_color=GREY_A, fill_opacity=0.55)
            return Intersection(lit, screen, stroke_width=0, fill_color=GREY_A, fill_opacity=0.55)

        bright = always_redraw(edge)
        # the neuron and its spikes
        soma = Circle(radius=0.32, stroke_color=KERNEL, stroke_width=2.5, fill_color=KERNEL, fill_opacity=0.2)
        soma.move_to([2.2, 0.9, 0])
        dend = VGroup(*[Line(soma.get_center() + 0.32 * np.array([np.cos(a), np.sin(a), 0]),
                             soma.get_center() + 0.85 * np.array([np.cos(a), np.sin(a), 0]), color=KERNEL,
                             stroke_width=2) for a in (2.2, 2.9, 3.6, 4.2)])
        axon = Line(soma.get_right(), soma.get_right() + RIGHT * 2.6, color=KERNEL, stroke_width=2)
        nl = label(r"one neuron", font_size=20, color=KERNEL).next_to(soma, UP, buff=0.45)
        t_ax = Line([0.6, -1.4, 0], [6.4, -1.4, 0], color=GREY_C, stroke_width=2)
        tl = label(r"its spikes, \ in time", font_size=20, color=GREY_B).next_to(t_ax, DOWN, buff=0.15)
        g = np.random.default_rng(1959)  # illustrative spike times: a few at random, a burst as the edge passes
        quiet = np.sort(g.uniform(0.6, 6.4, 6))
        burst = np.sort(g.uniform(3.4, 4.6, 26))

        def spikes(times, h=0.55):
            return VGroup(*[Line([t, -1.4, 0], [t, -1.4 + h, 0], color=KERNEL, stroke_width=2) for t in times])

        sq, sb = spikes(quiet), spikes(burst)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "In the late 1950s, at Johns Hopkins, David Hubel and Torsten Wiesel were recording from single neurons "
            "in the visual cortex of a cat, while it looked at a screen. <bookmark mark='a'/> Spots of light, "
            "their stimulus of the day, did almost nothing. <bookmark mark='b'/> Then, as Hubel told it, while they "
            "slid a glass slide into the projector, the faint straight shadow of its edge swept across the screen, "
            "<bookmark mark='c'/> and the cell began to fire in a burst. It wanted an edge, at one particular "
            "angle, in one particular place."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(screen), FadeIn(sl), FadeIn(tag))
            self.play(FadeIn(soma), Create(dend), Create(axon), FadeIn(nl), Create(t_ax), FadeIn(tl))
            vo.wait_until("a")
            dots = VGroup(*[Dot(screen.get_center() + np.array([dx, dy, 0]), radius=0.12, color=GREY_A)
                            for dx, dy in ((-1.1, 0.6), (0.8, -0.5), (0.2, 0.9))])
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.4),
                      LaggedStart(*[Create(s) for s in sq], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(dots))
            self.add(bright)
            vo.wait_until("c")
            self.play(x.animate.set_value(2.0), LaggedStart(*[Create(s) for s in sb], lag_ratio=0.08),
                      Flash(soma, color=KERNEL, line_length=0.3), run_time=3.0)
        bright.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        o, cf = load("orientation"), load("cifar")
        W = np.asarray(o["w1"])
        tiles = grid_of([img_filter(w, 0.7) for w in W], cols=8, buff=0.08).move_to([-2.4, -0.2, 0])
        frame = SurroundingRectangle(tiles, color=GREY_D, buff=0.12, stroke_width=1.2)
        cg = np.asarray(load("data")["cifar_grid"])  # (10 classes, 8 photographs, 32, 32, 3)
        photos = Group(*[img_rgb(cg[(r * 7 + c) % 10, (r + c) % 8], 0.56) for r in range(5) for c in range(7)])
        photos.arrange_in_grid(rows=5, cols=7, buff=0.06).move_to(tiles)
        head = label(rf"the ${len(W)}$ first-layer filters of a network trained on this computer", font_size=26,
                     color=CNN).to_edge(UP, buff=0.45)
        mins = cf["seconds"] / 60
        facts = VGroup(
            label(r"CIFAR-10: \ $50{,}000$ small photographs", font_size=24, color=GREY_A),
            label(rf"${cf['epochs']}$ passes, \ about ${mins:.0f}$ minutes", font_size=24, color=GREY_A),
            label(rf"${o['n_oriented']}$ of ${o['n']}$ pick out an edge \\ at one orientation", font_size=26,
                  color=KERNEL),
            label(r"nobody told it about edges", font_size=26, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.2, -0.2, 0])
        keep_in_frame(facts)
        with self.voiceover(
            "Half a century later, here is a network trained on the computer making this video. "
            f"It looked at fifty thousand small photographs, {cf['epochs']} times over, for about {mins:.0f} "
            "minutes. <bookmark mark='a'/> These are the filters its first layer grew. "
            f"<bookmark mark='b'/> {o['n_oriented']} of the {o['n']} pick out an edge at one orientation, like "
            "Hubel and Wiesel's cell. Nobody told it about edges. It found them because they were useful."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(facts[0]), LaggedStart(*[FadeIn(p) for p in photos], lag_ratio=0.03), run_time=1.6)
            self.play(FadeIn(facts[1]))
            vo.wait_until("a")
            self.play(FadeOut(photos), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tiles], lag_ratio=0.03), Create(frame),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(facts[2], shift=UP * 0.1))
            self.play(FadeIn(facts[3], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def remember(self):
        s = load("seq2seq")
        run = s["runs"]["1-0"]
        al = np.asarray(run["show_alpha"])  # (outputs, inputs)
        word = s["show"]
        out = run["show_out"]
        n_in = len(word)
        al = al[:len(out) + 1, :n_in]
        hm = img_heat(al, 4.6, sym=False, pos=ATT, height=4.6 * al.shape[0] / al.shape[1]).move_to([2.2, -0.4, 0])
        cw = hm.width / n_in
        ch = hm.height / al.shape[0]
        xs = VGroup(*[data_text(c, font=MONO_FONT, font_size=22, color=GREY_A).move_to(
            hm.get_corner(UL) + np.array([cw * (i + 0.5), 0.3, 0])) for i, c in enumerate(word)])
        ys = VGroup(*[data_text(c, font=MONO_FONT, font_size=22, color=LSTMC).move_to(
            hm.get_corner(UL) + np.array([-0.3, -ch * (i + 0.5), 0])) for i, c in enumerate(out + "|")])
        ys[-1].set_opacity(0)
        il = label(r"reads", font_size=22, color=GREY_B).next_to(xs, UP, buff=0.15)
        ol = label(r"writes", font_size=22, color=LSTMC).next_to(ys, LEFT, buff=0.2)
        hc = history_card(2014, r"Sutskever, Vinyals \& Le; \ Cho et al.; \ Bahdanau, Cho \& Bengio",
                          r"networks that read a sentence and write its translation; \ then, attention",
                          width=4.6, color=HIST).to_edge(LEFT, buff=0.3).shift(UP * 0.4)
        tag = note(r"computed: \ our encoder--decoder, \ trained here to reverse strings").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Seeing is half of this part. The other half is remembering. <bookmark mark='a'/> In 2014 networks "
            "learned to read a whole sentence and write it in another language. <bookmark mark='b'/> And that year "
            "they learned to look back: at each word they wrote, to pick out the words of the input they needed. "
            "This is a small one, trained here to write strings backwards; the bright squares are where it looked. "
            "It was the first attention."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(xs), FadeIn(il), FadeIn(ys), FadeIn(ol), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(hm), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"How did machines learn to see, \\ and to remember?", font_size=46).move_to(UP * 1.6)
        steps = [(r"Hubel \& Wiesel", HIST), (r"the Neocognitron", HIST), (r"LeNet", CNN), (r"ImageNet", HIST),
                 (r"AlexNet", CNN), (r"ResNet", CNN), (r"recurrent nets", LSTMC), (r"the LSTM", LSTMC),
                 (r"seq2seq", LSTMC), (r"attention", ATT), (r"recurrence returns", LSTMC)]
        row1 = VGroup()
        for i, (t, c) in enumerate(steps[:6]):
            row1.add(label(t, font_size=24, color=c))
            if i < 5:
                row1.add(MathTex(r"\to", font_size=30, color=GREY_C))
        row2 = VGroup()
        for i, (t, c) in enumerate(steps[6:]):
            row2.add(label(t, font_size=24, color=c))
            if i < 4:
                row2.add(MathTex(r"\to", font_size=30, color=GREY_C))
        row1.arrange(RIGHT, buff=0.2).move_to(DOWN * 0.1)
        row2.arrange(RIGHT, buff=0.2).move_to(DOWN * 1.2)
        for r in (row1, row2):
            if r.width > 13.2:
                r.width = 13.2
        strip = timeline(lit=(1986, 1991, 1997, 1998, 2009, 2012, 2015, 2017)).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "How did machines learn to see, and to remember? <bookmark mark='a'/> We'll follow the path from "
            "Hubel and Wiesel's cells to LeNet, ImageNet, and networks a hundred and fifty layers deep. "
            "<bookmark mark='b'/> Then time: recurrent networks, the LSTM, translation, and the attention that grew "
            "out of it. <bookmark mark='c'/> And we'll train every kind "
            "of network we meet, on this computer, and watch it learn."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in row1], lag_ratio=0.12), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in row2], lag_ratio=0.12), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(strip))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Seeing and Remembering", font_size=44).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"vision before deep learning; \ convolution, \ translation equivariance, \ receptive fields",
            r"LeNet and MNIST; \ ImageNet and AlexNet; \ why it won; \ VGG, Inception, ResNet",
            r"what the filters learn; \ adversarial examples; \ cheaper convolutions, \ ConvNeXt",
            r"recurrent networks: \ backpropagation through time, \ vanishing and exploding gradients",
            r"the LSTM and the GRU; \ a character LSTM on our scoreboard",
            r"sequence to sequence, \ beam search; \ Bahdanau's attention; \ recurrence returns",
        ], font_size=26)
        with self.voiceover(
            "This is Part 10 of AI, Built, in the second act, learning from data: after Part 9's networks, and "
            "before Part 11's optimizers. <bookmark mark='a'/> Here is the plan: vision before deep learning, and "
            "the convolution that replaced it; the deep networks, what they learn, and how to fool them; then "
            "memory, from the LSTM to attention, and back."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()


MONO_FONT = "DejaVu Sans Mono"
