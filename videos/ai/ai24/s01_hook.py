from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (DIGIT, DINO_C, Hypersphere, JEPA, MAE_C, NAIVE, PART, POS, SIMCLR, digit_sheet,
                                   load, node_box, pct, tag)


class Hook(VoiceoverScene):
    def construct(self):
        self.sphere()
        self.replay()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def sphere(self):
        sp = load("sphere")
        Z = np.asarray(sp["simclr_z"])
        lab = np.asarray(sp["labels"]).astype(int)
        hs = Hypersphere(Z[-1], [DIGIT[c] for c in lab], radius=2.7, center=[-2.2, -0.2, 0], dot=0.05)
        key = VGroup(*[VGroup(Dot(radius=0.07, color=DIGIT[c]), MathTex(str(c), font_size=30, color=DIGIT[c]))
                       .arrange(RIGHT, buff=0.12) for c in range(10)]).arrange_in_grid(5, 2, buff=(0.5, 0.22))
        key.move_to([4.6, 1.2, 0])
        key_h = label(r"colour: \ the digit's label", font_size=22, color=GREY_A).next_to(key, UP, buff=0.25)
        never = label(r"never shown to the network", font_size=22, color=NAIVE).next_to(key, DOWN, buff=0.25)
        zk = float(sp["simclr_zknn"])
        acc = VGroup(label(r"nearest neighbours on the sphere \\ name the digit", font_size=22, color=GREY_A),
                     MathTex(pct(zk) + r"\%", font_size=44, color=POS)).arrange(DOWN, buff=0.15)
        acc.next_to(never, DOWN, buff=0.5)
        tg = tag(r"computed: \ trained on this computer, \ MNIST test digits")
        with self.voiceover(
            "These six hundred dots are handwritten digits. A network has squeezed each one into just three "
            "numbers, a point on a sphere. <bookmark mark='a'/> The colours are the digits' labels, zero to nine. "
            "<bookmark mark='b'/> But the network never saw a label. All it was ever asked was which two distorted "
            "copies of a picture came from the same digit. <bookmark mark='c'/> And yet, ask a digit's nearest "
            f"neighbours on this sphere what it is, and they are right {pct(zk, 0)} percent of the time."
        ) as vo:
            self.add(hs)
            self.play(FadeIn(hs), run_time=1.0)
            self.play(hs.angle.animate.set_value(0.9), run_time=vo.until("a"), rate_func=linear)
            self.play(FadeIn(key_h), LaggedStart(*[FadeIn(k) for k in key], lag_ratio=0.08),
                      hs.angle.animate.set_value(1.4), run_time=2.0, rate_func=linear)
            self.play(hs.angle.animate.set_value(1.9), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(never, shift=UP * 0.1), hs.angle.animate.set_value(2.4), run_time=1.5, rate_func=linear)
            self.play(hs.angle.animate.set_value(3.2), run_time=vo.until("c"), rate_func=linear)
            self.play(FadeIn(acc, shift=UP * 0.1), FadeIn(tg), hs.angle.animate.set_value(3.8), run_time=1.5,
                      rate_func=linear)
            self.play(hs.angle.animate.set_value(4.6), run_time=max(0.5, vo.remaining()), rate_func=linear)
        hs.freeze()
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        sp = load("sphere")
        Z = np.asarray(sp["simclr_z"])
        lab = np.asarray(sp["labels"]).astype(int)
        steps = np.asarray(sp["rec_steps"])
        hs = Hypersphere(Z, [DIGIT[c] for c in lab], radius=2.6, center=[-2.6, -0.3, 0], dot=0.045)
        hs.angle.set_value(0.6)
        head = label(r"Training, replayed", font_size=34).to_corner(UL, buff=0.4)
        sl = always_redraw(lambda: label(
            rf"step ${steps[int(np.clip(round(hs.t.get_value()), 0, len(steps) - 1))]}$ \ of \ ${steps[-1]}$",
            font_size=24, color=GREY_A).move_to([3.4, 2.6, 0]))
        Zn = load("sphere")
        al, un = np.asarray(Zn["simclr_align"]), np.asarray(Zn["simclr_unif"])
        side = VGroup(
            label(r"two views of one digit \\ $\to$ the same spot", font_size=24, color=POS),
            label(r"different digits \\ $\to$ spread over the sphere", font_size=24, color=SIMCLR),
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([3.6, 0.2, 0])
        nv = load("sphere")
        Zc = np.asarray(nv["naive_z"])
        hs2 = Hypersphere(Zc[-1], [DIGIT[c] for c in lab], radius=1.1, center=[4.4, -2.4, 0], dot=0.03)
        cap2 = label(r"pull together, \ and nothing else", font_size=20, color=NAIVE).next_to(hs2, LEFT, buff=0.25)
        P0 = Z[0] / np.linalg.norm(Z[0], axis=1, keepdims=True)
        bunched = float(np.linalg.norm(P0.mean(0))) > 0.9
        start = ("At the start, the untrained network puts almost every digit on the same small patch of the sphere."
                 if bunched else "At the start the points are scattered at random.")
        i_b = int(np.searchsorted(steps, 30))
        with self.voiceover(
            f"Here is how it got there. {start} <bookmark mark='a'/> Each "
            "step shows the network a hundred and twenty-eight digits, each in two versions, cropped, tilted, "
            "smudged. It pulls the two versions of each digit together, <bookmark mark='b'/> and pushes everything "
            "else apart. Nothing in this rule mentions a five or a seven. <bookmark mark='c'/> The clusters appear "
            "anyway, because two smudged copies of a five resemble each other in the same ways that all fives "
            "resemble each other. <bookmark mark='d'/> Leave out the push, and the network finds a lazier answer: "
            "every digit on the same spot."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hs), FadeIn(sl))
            vo.wait_until("a")
            self.play(FadeIn(side[0], shift=UP * 0.1))
            self.play(hs.t.animate.set_value(i_b), hs.angle.animate.set_value(1.6),
                      run_time=max(1.0, vo.until("b") - 0.2), rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side[1], shift=UP * 0.1))
            self.play(hs.t.animate.set_value(len(steps) - 1), hs.angle.animate.set_value(3.6),
                      run_time=max(4.0, vo.until("d") - 0.3), rate_func=lambda u: u ** 0.6)
            vo.wait_until("d")
            self.play(FadeIn(hs2), FadeIn(cap2))
            self.play(hs2.angle.animate.set_value(2.0), hs.angle.animate.set_value(4.6),
                      run_time=max(0.5, vo.remaining()), rate_func=linear)
        hs.freeze()
        hs2.freeze()
        sl.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        v = load("views")
        orig = np.asarray(v["orig"])
        full = np.asarray(v["full"])
        q = label(r"How does a network learn what matters \\ when nobody labels the data?", font_size=40)
        q.to_edge(UP, buff=0.5)
        ways = VGroup(
            node_box(r"hide part of it, \ predict it", MAE_C, font_size=24),
            node_box(r"two views must agree", SIMCLR, font_size=24),
            node_box(r"predict what the hidden part means", JEPA, font_size=24),
        ).arrange(DOWN, buff=0.45).move_to([3.2, -0.6, 0])
        pics = Group()
        # a digit with its lower half hidden; two views of one digit; a digit and a hidden block, its meaning marked
        d0 = orig[5].astype(float).copy()
        hid = d0.copy()
        hid[14:] = 0
        pics.add(Group(digit_sheet([d0 / 255.0, hid / 255.0], 1, 2, size=0.8, gap=0.1)))
        pics.add(Group(digit_sheet([full[0, 5], full[1, 5]], 1, 2, size=0.8, gap=0.1, color=SIMCLR)))
        h2 = d0.copy()
        h2[8:20, 8:20] = 0
        pics.add(Group(digit_sheet([h2 / 255.0], 1, 1, size=0.8), MathTex(r"\to f(\,\cdot\,)", font_size=30,
                                                                         color=JEPA)).arrange(RIGHT, buff=0.15))
        for p_, w_ in zip(pics, ways):
            p_.next_to(w_, LEFT, buff=0.5)
        Group(*pics, *ways).move_to([0, -0.6, 0])
        trap = label(r"the trap: \ the same answer for every input", font_size=26, color=NAIVE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "That is the question of this part: how does a network learn what matters when nobody labels the data? "
            "<bookmark mark='a'/> The field has found three families of answers. Hide part of the input and ask "
            "for it back. <bookmark mark='b'/> Show two versions of the same input and ask the network to make them "
            "agree. <bookmark mark='c'/> Or hide part of the input and ask not for its pixels but for what it "
            "means. <bookmark mark='d'/> And every one of them must avoid the same trap we just saw: a network that "
            "gives the same answer for everything agrees with itself perfectly."
        ) as vo:
            self.play(Write(q), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(ways[0], shift=LEFT * 0.2), FadeIn(pics[0]))
            vo.wait_until("b")
            self.play(FadeIn(ways[1], shift=LEFT * 0.2), FadeIn(pics[1]))
            vo.wait_until("c")
            self.play(FadeIn(ways[2], shift=LEFT * 0.2), FadeIn(pics[2]))
            vo.wait_until("d")
            self.play(FadeIn(trap, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Learning Without Labels", font_size=44).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.5)
        obj = objectives_card([
            r"how we got here, \ and how to judge a representation; \ pretext puzzles",
            r"contrastive learning: \ from word2vec's negatives to InfoNCE, \ SimCLR and MoCo",
            r"the hypersphere: \ temperature, \ alignment and uniformity",
            r"collapse, \ computed and prevented: \ BYOL, \ SimSiam, \ Barlow Twins, \ VICReg",
            r"self-distillation: \ DINO, \ and scaling it with curated data",
            r"masked modelling and JEPA: \ MAE, \ BEiT, \ I-JEPA, \ V-JEPA 2",
            r"every method on one budget; \ embeddings for search, \ Matryoshka",
            r"comparing representations: \ CKA, \ and the platonic hypothesis",
        ], font_size=24)
        with self.voiceover(
            "This is Part 24 of AI, Built: learning without labels. <bookmark mark='a'/> In this part: how the "
            "field got here, and how to judge what a network has learned; <bookmark mark='o2'/> contrastive "
            "learning, from word2vec's negative samples to SimCLR; <bookmark mark='o3'/> the geometry of the "
            "sphere; <bookmark mark='o4'/> collapse, made to happen and then prevented four ways; <bookmark "
            "mark='o5'/> self-distillation, and what it takes to scale it; <bookmark mark='o6'/> masked models and "
            "joint-embedding prediction; <bookmark mark='o7'/> every method on one budget, and embeddings for "
            "search; <bookmark mark='o8'/> and whether different networks end up seeing the world the same way. "
            "Every model in this part is trained on the computer making it."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            veils = VGroup(*[Rectangle(width=r_.width + 0.3, height=r_.height + 0.14, stroke_width=0,
                                       fill_color=config.background_color, fill_opacity=0.72).move_to(r_)
                             for r_ in obj.rows])
            mark = Triangle(color=C.BITS, fill_opacity=1, stroke_width=0).rotate(-PI / 2).scale(0.1)
            mark.next_to(obj.rows[0], LEFT, buff=0.15)
            self.play(FadeOut(smap), FadeOut(title), FadeIn(obj), FadeIn(veils[1:]), FadeIn(mark))
            for k, mk in enumerate(["o2", "o3", "o4", "o5", "o6", "o7", "o8"], 1):
                vo.wait_until(mk)
                self.play(FadeOut(veils[k]), mark.animate.next_to(obj.rows[k], LEFT, buff=0.15), run_time=0.5)
            self.play(FadeOut(mark), run_time=0.4)
        self.wait(0.3)
        self.clear_scene()
