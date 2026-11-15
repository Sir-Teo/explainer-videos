from __future__ import annotations

import numpy as np

from videos.music.music61.common import *  # noqa: F403


class Network(SoundScene):
    def construct(self):
        chapter(self, 6, r"A network that listens", r"What can a machine learn from examples that it cannot be told?")
        self.design()
        self.training()
        self.result()
        self.inside()
        self.heard()

    # ------------------------------------------------------------------
    def design(self):
        def layer(n, x, col, txt):
            dots = VGroup(*[Circle(radius=0.08, stroke_color=col, stroke_width=2) for _ in range(n)]).arrange(DOWN, buff=0.12).move_to([x, 0.1, 0])
            return VGroup(dots, label(txt, font_size=15, color=col).next_to(dots, DOWN, buff=0.25))
        L = VGroup(layer(11, -5.0, GREY_B, r"5 frames \ $\times$ 217 bins"), layer(9, -1.8, BLUE, r"256 units"), layer(9, 1.4, BLUE, r"256 units"),
                   layer(7, 4.6, TUNE, r"37 notes: \ a probability each"))
        edges = VGroup()
        for a, b in zip(L[:-1], L[1:]):
            for p in a[0][::2]:
                for q in b[0][::2]:
                    edges.add(Line(p.get_center(), q.get_center(), stroke_width=0.6, color=GREY_D))
        eq = MathTex(r"\hat y = \sigma\!\big(W_3\,\mathrm{relu}(W_2\,\mathrm{relu}(W_1 x))\big), \qquad \mathcal{L} = -\sum_k \big[w\,y_k\log\hat y_k + (1 - y_k)\log(1 - \hat y_k)\big]",
                     font_size=28, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"a small transcription network", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The other route is to learn from examples. <bookmark mark='a'/> Monochord's network is small: it reads five "
            "neighbouring frames of the log-frequency spectrogram, passes them through two layers of two hundred and fifty-six "
            "units, and outputs, for each of the thirty-seven notes from C3 to C6, the probability that it is sounding. "
            "<bookmark mark='b'/> It is trained by binary cross-entropy against the answer key, with the rare positive frames "
            "weighted up. Nobody tells it what a partial is."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(edges), LaggedStart(*[FadeIn(l) for l in L], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(eq))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        d = load("net")
        data = load("data")
        loss = np.array(d["losses"])
        ax = frame_axes(width=6.0, height=2.6, xlo=0, xhi=len(loss) - 1, ylo=0, yhi=loss.max() * 1.05, center=DOWN * 0.9 + RIGHT * 2.8)
        cv = curve(np.arange(len(loss)), loss, ax.to, color=TUNE, width=3)
        xl = label(r"epochs", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.1)
        yl = label(r"training loss", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.1)
        facts = VGroup(
            label(rf"{data['train_pieces']} pieces of random polyphony, \ 6 seconds each", font_size=18, color=WHITE),
            label(rf"{data['train_notes']:,} notes, \ {d['frames']:,} frames", font_size=18, color=WHITE),
            label(r"all on one instrument: \ Part 38's piano", font_size=18, color=TUNE),
            label(r"every answer exact, \ because Monochord played it", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(LEFT * 3.4 + DOWN * 0.6)
        head = label(r"training on rendered music", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"The training set is what Monochord can do and the field mostly cannot: {say(data['train_pieces'])} pieces of random "
            f"polyphony, six seconds each, {say(data['train_notes'])} notes, every one with an exact answer, because Monochord "
            "played it. <bookmark mark='a'/> All on one instrument, Part 38's piano. <bookmark mark='b'/> The loss falls over "
            "the epochs, and the network has learnt what a piano note looks like from the inside."
        ) as vo:
            self.play(FadeIn(head), FadeIn(facts[0]), FadeIn(facts[1]), FadeIn(facts[3]))
            vo.wait_until("a")
            self.play(FadeIn(facts[2]))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(cv), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        n, m = load("nmf")["scores"]["piano"], load("net")["scores"]["piano"]
        g = VGroup()
        for name, a, b in ((r"note F-measure", n["f"], m["f"]), (r"precision", n["precision"], m["precision"]), (r"recall", n["recall"], m["recall"])):
            g.add(VGroup(label(name, font_size=20, color=WHITE), label(f"{a:.2f}", font_size=22, color=GREY_B), label(f"{b:.2f}", font_size=22, color=TUNE)))
        g.arrange(DOWN, buff=0.45)
        for r in g:
            r[0].set_x(-3.0)
            r[1].set_x(0.8)
            r[2].set_x(3.6)
        top = VGroup(label(r"NMF", font_size=18, color=GREY_B).move_to([0.8, g.get_top()[1] + 0.5, 0]),
                     label(r"the network", font_size=18, color=TUNE).move_to([3.6, g.get_top()[1] + 0.5, 0]))
        note = label(rf"12 test pieces on the piano, \ never seen in training; \ the network's frame F-measure: \ {m['frame_f']:.2f}", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"on new piano pieces", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        better = m["f"] > n["f"]
        with self.voiceover(
            f"On twelve new piano pieces, never heard in training: <bookmark mark='a'/> the factorization's note F-measure is "
            f"{say(n['f'], 2)}; <bookmark mark='b'/> the network's, {say(m['f'], 2)}. "
            + ("Learning from examples wins on the instrument it learnt." if better else "Here the factorization holds its own.")
            + " But both were trained on this piano. The real test is a timbre neither has heard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*[r[0] for r in g])), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(top[0]), FadeIn(VGroup(*[r[1] for r in g])))
            vo.wait_until("b")
            self.play(FadeIn(top[1]), FadeIn(VGroup(*[r[2] for r in g])))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("net")
        c = clip("net.piano")
        P = np.array(d["piano_P"])
        hop = 2 * 960 / 48000
        dur = P.shape[1] * hop
        w, h = 10.5, 3.6
        pic = picture(P, 0, 1, w, h).move_to(DOWN * 0.2)
        x0, y0 = pic.get_left()[0], pic.get_bottom()[1]
        ph = h / P.shape[0]
        truth = VGroup(*[Rectangle(width=max(0.03, w * (b - a) / dur), height=ph * 0.9, stroke_color=WHITE, stroke_width=1.2, fill_opacity=0)
                         .move_to([x0 + w * (a + b) / 2 / dur, y0 + ph * (m - 48 + 0.5), 0]) for m, a, b in d["piano_truth"]])
        ps = d["piano_scores"]
        note = label(rf"the network's probabilities \ (bright: \ sure); \ white boxes: \ the notes played. \ This piece: \ F = {ps['f']:.2f}", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.3)
        head = label(r"what the network hears", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is the same piano test piece the factorization heard in Chapter 5, now as the network hears it: its probability for every note in every frame."):
            self.play(FadeIn(head), FadeIn(pic), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"a test piece", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            line = Line(pic.get_corner(DL), pic.get_corner(UL), color=WHITE, stroke_width=2)
            snd.show(line)
            snd.drive(line, lambda m, t: m.move_to([x0 + w * min(t, dur) / dur, pic.get_center()[1], 0]))
        with self.voiceover(
            "Compared with the factorization's activations, the picture is cleaner: the network has learnt to stay quiet on "
            f"the octaves and twelfths that share a note's partials. Note by note it scores {say(ps['f'], 2)} on this piece."
        ):
            self.play(Create(truth), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inside(self):
        d = load("net")
        pics = Group()
        for i, u in enumerate(d["units"]):
            w = np.array(u["w"])
            pic = picture(w, -1, 1, 1.1, 3.0)
            pics.add(Group(pic, label(rf"near MIDI {u['peak_midi']:.0f}", font_size=12, color=GREY_A).next_to(pic, DOWN, buff=0.1)))
        pics.arrange(RIGHT, buff=0.55).move_to(DOWN * 0.3)
        note = label(r"six of the 256 first-layer units: \ their weights over 5 frames \ (across) \ and 217 log-frequency bins \ (up); \ bright: \ positive, \ dark: \ negative", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.3)
        head = label(r"inside the network", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "What has it learnt? <bookmark mark='a'/> Here are six of the first layer's two hundred and fifty-six units, the "
            "ones with the largest weights: each is a pattern over five frames and the log-frequency bins. "
            "<bookmark mark='b'/> Many are combs, bright at a set of partials and dark between them: learnt templates, like "
            "NMF's, but with negative weights too, so a unit can say not this note as well as this one. Some respond to a change "
            "from frame to frame: an onset. Nobody wrote either down."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pics], lag_ratio=0.2), FadeIn(note), run_time=1.5)
            vo.wait_until("b")
            self.play(Indicate(pics, color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()
