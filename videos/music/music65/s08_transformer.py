from __future__ import annotations

import numpy as np

from videos.music.music65.common import *  # noqa: F403


class Transformer(SoundScene):
    def construct(self):
        chapter(self, 7, r"A transformer", r"Can a network do better than counting, \ with so little music?")
        self.design()
        self.curves()
        self.scores()
        self.memorized()
        self.samples()

    # ------------------------------------------------------------------
    def design(self):
        d = load("transformer")
        items = [
            (r"\textit{AI, Built}'s pocket transformer: \ attention over everything so far, \ rotary positions, \ three layers", WHITE),
            (rf"{d['plain']['params']:,} weights; \ trained to predict the next token, \ as a language model is", WHITE),
            (rf"the training tunes alone: \ {d['plain']['train_tokens']:,} tokens, \ far fewer than weights", WHITE),
            (rf"or each tune in twelve keys, \ transposed: \ {d['aug']['train_tokens']:,} tokens \ (an old trick: \ data augmentation)", WHITE),
            (r"a few tunes kept aside to watch while training; \ the test tunes are touched only at the end", TUNE),
        ]
        rows_scene(self, r"Monochord's transformer", items,
                   "Now a network. <bookmark mark='b'/> It is the pocket transformer of AI, Built: each token attends to everything "
                   "before it, positions are rotations, and there are three layers. <bookmark mark='c'/> It has about "
                   f"{say(round(d['plain']['params'] / 1000))} thousand weights, trained to predict the next token, exactly as a "
                   "language model is. <bookmark mark='d'/> The training tunes alone make only "
                   f"{say(round(d['plain']['train_tokens'] / 1000))} thousand tokens, far fewer than the weights. "
                   "<bookmark mark='e'/> So train a second copy on each tune in twelve keys, transposed: "
                   f"{say(round(d['aug']['train_tokens'] / 1000))} thousand tokens, by the old trick of data augmentation. "
                   "<bookmark mark='f'/> A few tunes are kept aside to watch during training; the test tunes are touched only at "
                   "the end.", marks="bcdef")

    # ------------------------------------------------------------------
    def curves(self):
        d = load("transformer")
        cp = np.array(d["plain"]["curve"])
        ca = np.array(d["aug"]["curve"])
        top = max(cp[:, 1].max(), ca[:, 1].max()) * 1.05
        ax = frame_axes(width=8.0, height=3.2, xlo=0, xhi=max(cp[:, 0].max(), ca[:, 0].max()), ylo=0, yhi=top, center=DOWN * 0.4 + LEFT * 0.8)
        c1 = curve(cp[:, 0], cp[:, 1], ax.to, color=EAR, width=3)
        c2 = curve(ca[:, 0], ca[:, 1], ax.to, color=TUNE, width=3)
        xl = label(r"training steps", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"loss on the tunes set aside \ (nats per token)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        key = VGroup(label(r"tunes alone", font_size=16, color=EAR), label(r"tunes in twelve keys", font_size=16, color=TUNE)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(RIGHT, buff=0.6)
        i = int(np.argmin(cp[:, 1]))
        head = label(r"training", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        ia = int(np.argmin(ca[:, 1]))
        with self.voiceover(
            "Watch both learn, scored on the tunes set aside. <bookmark mark='a'/> On the tunes alone the loss falls, then "
            f"turns round near step {say(int(cp[i, 0]))} and climbs: the network has begun to learn its training tunes by "
            "heart, and every step of memorizing makes it worse on new ones. <bookmark mark='b'/> In twelve keys it turns "
            f"later, near step {say(int(ca[ia, 0]))}: no single key's tunes can be memorized as fast, so it "
            "must learn intervals and patterns that hold in any key, though in the end it memorizes too. Each model is kept "
            "as it was where the tunes set aside said to stop."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(c1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(c2), run_time=1.5)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scores(self):
        d = load("transformer")
        rows = [(r"Markov chain, \ order 2 \ (the best order)", d["markov2"], None, GREY_B),
                (r"transformer, \ tunes alone", d["plain"]["bits"], d["plain"], EAR),
                (r"transformer, \ twelve keys", d["aug"]["bits"], d["aug"], TUNE)]
        top = max(r[1] for r in rows)
        g = VGroup()
        for name, b, s, col in rows:
            extra = label(rf"copies runs of {s['longest']:.0f} notes" if s else r"", font_size=15, color=GREY_A)
            g.add(VGroup(label(name, font_size=18, color=col), Rectangle(width=5.0 * b / top, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.8),
                         label(f"{b:.2f} bits", font_size=17, color=WHITE), extra))
        g.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(LEFT * 1.4 + DOWN * 0.2)
        for r in g:
            r[1].next_to(r[0], RIGHT, buff=0.3).align_to(g, LEFT).shift(RIGHT * 4.8)
            r[2].next_to(r[1], RIGHT, buff=0.2)
            r[3].next_to(r[2], RIGHT, buff=0.3)
        note = label(r"bits per note on the test tunes: \ lower is better", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"against counting", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        p, a, m = d["plain"]["bits"], d["aug"]["bits"], d["markov2"]
        verdict = "beats" if a < m else "does not beat"
        with self.voiceover(
            f"On the test tunes the best counting model needs {say(m, 2)} bits a note. <bookmark mark='a'/> The transformer "
            f"trained on the tunes alone, stopped at its best, needs {say(p, 2)}. <bookmark mark='b'/> In twelve keys, "
            f"{say(a, 2)}: better, and it {verdict} the order-two chain. With a few thousand notes to learn from, the network "
            "has little room to show what it can do; the field's networks learn from many thousands of pieces, where counting "
            "cannot follow."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note), FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1]))
            vo.wait_until("b")
            self.play(FadeIn(g[2]))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memorized(self):
        d = load("transformer")
        c = clip("plain.two")
        mm = d["memorized"]
        boxes = choice_boxes([r"the tunes-alone transformer, \ trained too long", rf"{bwv(mm['source'])}, \ by Bach"], width=4.6, height=0.9, buff=0.8, size=18).move_to(UP * 0.6)
        res = label(rf"{mm['copy']['length']} notes in a row from one chorale", font_size=20, color=EAR).next_to(boxes, DOWN, buff=0.6)
        head = label(r"a network that memorized", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("The memorizing is audible. Hear a tune from the network trained on the tunes alone for all fifteen hundred steps, far past where it should have stopped, then the chorale it copies most."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"network, \ then Bach", kind="synthesized", detail=rf"the transformer; \ {bwv(mm['source'])}", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["sample"], st["source"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["source"], c.duration, buff=0.08)
        with self.voiceover(
            f"{say(mm['copy']['length'])} notes in a row from {bwv_said(mm['source'])}. A network can memorize as an order-eight "
            "chain does, and more quietly: nothing in its weights says which tune it is reciting. Large music and language "
            "models have been shown to reproduce training data word for word, and measuring this is now part of how they are "
            "tested."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def samples(self):
        d = load("samples")
        c = clip("samples.three")
        boxes = choice_boxes([rf"first \ ({d['keys'][0]})", rf"second \ ({d['keys'][1]})", rf"third \ ({d['keys'][2]})"], width=3.4, height=0.9, buff=0.5, size=17).move_to(UP * 0.8)
        rolls = VGroup(*[tune_roll(x, width=3.4, height=1.0) for x in d["tunes"]]).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.8)
        res = label(rf"longest runs copied from a training tune: \ {', '.join(str(x) for x in d['copies'])} notes", font_size=17, color=TUNE).to_edge(DOWN, buff=0.45)
        head = label(r"the network, \ composing", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("And the network trained in twelve keys, composing from nothing: the first three tunes it drew, two phrases each. Because it learnt every key, it chooses one each time."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(rolls))
        st = d["starts"]
        ks = ["one", "two", "three"]
        with self.listen(c) as snd:
            window(snd, r"three tunes", kind="synthesized", detail=r"the transformer, \ twelve keys", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        with self.voiceover(
            f"Their longest copied runs are {', '.join(say(x) for x in d['copies'][:-1])} and {say(d['copies'][-1])} notes. They "
            "move like hymn tunes and end their phrases where hymn tunes do; they are no one's in particular."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()
