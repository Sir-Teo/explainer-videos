from __future__ import annotations

import numpy as np

from explainer.psychology.psyche.infer import SHAPES, TEXTURES
from videos.psychology.psych14.common import *  # noqa: F403


def thumbs(X, height=1.25, buff=0.25):
    g = Group(*[Group(picture(x, height), frame_box(picture(x, height))) for x in X])
    return g.arrange(RIGHT, buff=buff)


class Networks(VoiceoverScene):
    def construct(self):
        self.card()
        self.yamins()
        self.tiny()
        self.conflict()
        self.shuffled()

    def card(self):
        card = chapter_card(11, r"Deep networks as models", r"Does a network trained to recognize see as we do?",
                            lit={2014: r"Yamins", 2019: r"Geirhos"}, part=PART, scale=("mind", "circuit"),
                            marr=("what", "how"))
        with self.voiceover("Chapter eleven. Deep networks as models."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def yamins(self):
        head = heading(r"Trained to recognize, \ and brain-like")
        layers = VGroup()
        for k, (w, h, col) in enumerate(((0.3, 2.4, LIKE), (0.3, 2.0, LIKE), (0.3, 1.6, PRIOR), (0.3, 1.2, POST))):
            layers.add(Rectangle(width=w, height=h, color=col, fill_color=col, fill_opacity=0.35).move_to([k * 1.1, 0, 0]))
        names = VGroup(*[label(t, font_size=20, color=GREY_B).next_to(layers[k], DOWN, buff=0.15)
                         for k, t in enumerate((r"V1-like", r"V2", r"V4-like", r"IT-like"))])
        arrows = VGroup(*[Arrow(layers[k].get_right(), layers[k + 1].get_left(), buff=0.05, color=GREY_C,
                                stroke_width=2) for k in range(3)])
        net = VGroup(layers, names, arrows).move_to([-3.6, 0.4, 0])
        rows = rows_of([
            (r"a deep network: \ stacked layers of filters, \ pooling and nonlinearity, \ trained only to name objects", WHITE),
            (r"2014: \ Yamins, \ DiCarlo and colleagues: \ its top layer predicted 168 IT sites' responses to new images", POST),
            (r"its middle layers predicted V4; \ the better it recognized, \ the better it predicted", PRIOR),
            (r"nobody fitted the network to the neurons: \ the match came from the task", GREY_A),
        ], 6.4, 26, 0.34).move_to([3.2, 0.0, 0])
        keep_in_frame(rows)
        tag = published_tag(archive.YAMINS_2014.cite)
        with self.voiceover(
            "A deep convolutional network is a stack of layers. Each applies many small filters to the layer below, "
            "like Part 13's simple cells, then pools and rectifies, like complex cells and normalization. "
            "<bookmark mark='a'/> Train one, by gradient descent, to do nothing but name the objects in millions of "
            "photographs. <bookmark mark='b'/> In 2014, Daniel Yamins, James DiCarlo and colleagues recorded from "
            "168 sites in monkeys' inferior temporal cortex while the monkeys looked at thousands of images. Then "
            "they asked how well a trained network's top layer could predict those responses to images it hadn't been "
            "fitted on. It predicted them far better than any earlier model, accounting for about half of what was "
            "predictable at all. <bookmark mark='c'/> Its middle layers predicted the intermediate area V4. And "
            "across many networks, the better a network was at recognition, the better it predicted the neurons. "
            "<bookmark mark='d'/> Nobody fitted the network to the brain. The match came from training it on the same "
            "task. Part 60 takes up how far such models explain the brain. Here's one way they differ from us."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(net))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def tiny(self):
        d = load("cnn")
        head = heading(r"A small network, \ trained by us")
        ex = thumbs(d["examples"]).move_to([0, 1.6, 0])
        caps = VGroup(*[label(SHAPES[int(c)], font_size=20, color=GREY_B).next_to(t, DOWN, buff=0.1)
                        for t, c in zip(ex, d["example_labels"])])
        A = axes([0, 400], [0, 1.2], x_length=5.0, y_length=2.4, xticks=[0, 200, 400], yticks=[0, 0.6, 1.2],
                 xlabel=r"training step", ylabel=r"loss", center=[-3.2, -1.3, 0])
        ax = A.ax
        loss = curve(ax, np.arange(len(d["loss_paired"])), d["loss_paired"], POST, stroke_width=4)
        rows = rows_of([
            (r"three shapes, \ disc, \ square, \ triangle, \ each always filled with its own texture", WHITE),
            (r"one layer of eight 5-by-5 filters, \ pooled, \ then a readout: \ trained on 600 images", MODEL),
            (rf"on 300 new images: \ {pct(d['acc_paired'])} correct", POST),
        ], 6.0, 25, 0.32).move_to([3.4, -1.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ \texttt{infer.TinyConvNet}, \ in numpy")
        with self.voiceover(
            "In 2019, Robert Geirhos and colleagues found that networks trained on photographs rely on texture far "
            "more than people do. We can see why on a network small enough to train in seconds. "
            "<bookmark mark='a'/> Three shapes: a disc, a square and a triangle. In this training set, each shape "
            "always comes filled with its own texture: discs are striped, squares dotted, triangles checked. "
            "<bookmark mark='b'/> The network has one layer of eight five-by-five filters, averaged over the image, "
            "and a readout. We train it on six hundred images to name the shape. <bookmark mark='c'/> The loss falls "
            "quickly, and on three hundred new images it names the shape correctly every time. But which cue did it "
            "learn? In this training set, shape and texture always agree, so the scores can't tell us."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ex), FadeIn(caps), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(loss), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def conflict(self):
        d = load("cnn")
        head = heading(r"Shape or texture? \ Ask with a conflict")
        ex = thumbs(d["conflict"]).move_to([0, 1.5, 0])
        caps = VGroup()
        for t, s, tx, p in zip(ex, d["conflict_shape"], d["conflict_texture"], d["conflict_pred"]):
            col = TOUCH if int(p) == int(tx) else (POST if int(p) == int(s) else GREY_B)
            caps.add(VGroup(label(rf"{SHAPES[int(s)]}, \ {TEXTURES[int(tx)]}", font_size=17, color=GREY_B),
                            label(rf"says: \ {SHAPES[int(p)]}", font_size=19, color=col)).arrange(DOWN, buff=0.06)
                     .next_to(t, DOWN, buff=0.1))
        b = d["bias_paired"]
        bar = share_bar([b["texture"], b["shape"]], [TOUCH, POST], width=8.0, names=[r"texture", r"shape"])
        bar.move_to([0, -1.0, 0])
        bl = label(rf"300 conflict images: \ {b['texture']} answers follow the texture, \ {b['shape']} the shape",
                   font_size=26, color=WHITE).next_to(bar, DOWN, buff=0.25)
        rows = rows_of([
            (r"texture is local: \ a 5-by-5 filter sees it anywhere; \ shape needs the whole outline", PRIOR),
            (r"Geirhos and colleagues, \ 2019: \ ImageNet networks answer by texture; \ people, \ by shape", DATA),
        ], 12.4, 26, 0.26).to_edge(DOWN, buff=0.8)
        tag = VGroup(psyche_tag(r"computed: \ the network above, \ on cue-conflict images"),
                     published_tag(archive.GEIRHOS_2019.cite, corner=DL))
        with self.voiceover(
            "So ask with a conflict, as Geirhos did. <bookmark mark='a'/> Make images where shape and texture "
            "disagree: a disc filled with dots, a triangle with stripes. Each answer the network gives must follow "
            "one cue or the other. <bookmark mark='b'/> On three hundred conflict images, it followed the texture "
            "two hundred and eighty-three times, and the shape sixteen. It learned texture. "
            "<bookmark mark='c'/> That's not surprising once you think like the network. Texture is local: a small "
            "filter can detect stripes anywhere in the image. Shape depends on the whole outline. Given two cues "
            "that are equally good in the training data, gradient descent finds the easier one. "
            "<bookmark mark='d'/> Geirhos and colleagues found the same in large networks trained on the ImageNet "
            "photographs: on cue-conflict images, a cat's shape filled with an elephant's skin, the networks mostly "
            "said elephant. People, shown the same images, mostly said cat."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ex), LaggedStart(*[FadeIn(c) for c in caps], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bar), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def shuffled(self):
        d = load("cnn")
        head = heading(r"Change the diet, \ change the bias")
        b1, b2 = d["bias_paired"], d["bias_shuffled"]
        bar1 = share_bar([b1["texture"], b1["shape"]], [TOUCH, POST], width=7.0, names=[r"texture", r"shape"])
        bar2 = share_bar([b2["texture"], b2["shape"]], [TOUCH, POST], width=7.0, names=[r"texture", r"shape"])
        l1 = label(r"trained with each shape's own texture", font_size=24, color=GREY_A)
        l2 = label(r"trained with textures shuffled at random", font_size=24, color=GREY_A)
        g = VGroup(VGroup(l1, bar1).arrange(DOWN, buff=0.15), VGroup(l2, bar2).arrange(DOWN, buff=0.15))
        g.arrange(DOWN, buff=0.6).move_to([-2.2, 0.6, 0])
        v1 = label(rf"{pct(b1['texture_share'])} texture", font_size=24, color=TOUCH).next_to(bar1, RIGHT, buff=0.25)
        v2 = label(rf"{pct(b2['texture_share'])} texture", font_size=24, color=TOUCH).next_to(bar2, RIGHT, buff=0.25)
        rows = rows_of([
            (r"when texture is useless, \ the network must learn shape, \ and slowly does", WHITE),
            (rf"after the same training: \ {pct(d['acc_shuffled'])} correct, \ against a chance of 33\%", MODEL),
            (rf"on conflicts it now follows shape: \ {b2['shape']} answers to {b2['texture']}", POST),
            (r"the bias is in the data and the architecture, \ not in seeing itself; \ a property of networks, \ not of minds", PRIOR),
        ], 12.4, 26, 0.28).to_edge(DOWN, buff=0.8)
        tag = psyche_tag(r"computed: \ the same network, \ two training sets")
        with self.voiceover(
            "Is the texture bias in the network, or in what it was fed? <bookmark mark='a'/> Train the same network "
            "on images where the textures are shuffled at random, so that texture says nothing about the shape. "
            "<bookmark mark='b'/> Now the only way to succeed is to learn the shape, which is harder. After the same "
            "amount of training, it's right about half the time, where guessing would be right a third of the time. "
            "<bookmark mark='c'/> And on conflict images it now follows the shape: a hundred and forty-seven answers "
            "to sixty-six. <bookmark mark='d'/> Geirhos's group did the large version, training on photographs "
            "repainted in random artistic styles, and the networks became more shape-biased, and more robust to "
            "distortions. The bias is a property of the training data and the architecture. It tells us about "
            "networks, not about minds, but it's a warning: a model can match the brain's responses and still "
            "solve the problem a different way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(g[0]), FadeIn(v1))
            vo.wait_until("a")
            self.play(FadeIn(g[1]), FadeIn(v2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
