from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import CPUC, FLOPC, GPUC, PART, box_label, load
from videos.ai.ai17.specs import AI_AND_COMPUTE, ALEXNET_DAYS, ALEXNET_FLOP, GPUS


class AlexNet(VoiceoverScene):
    def construct(self):
        self.card()
        self.imagenet()
        self.two_gpus()
        self.arithmetic()
        self.aftermath()

    def card(self):
        card = chapter_card(4, r"AlexNet: the moment", r"What happened when deep learning met the GPU?", lit=(2012,),
                            part=PART)
        with self.voiceover("Chapter four. AlexNet: the moment."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def imagenet(self):
        hc = history_card(2009, r"Jia Deng, Fei-Fei Li and colleagues, \ ImageNet",
                          r"millions of labelled photographs; \ from 2010 a yearly contest on $1.2$ million of them "
                          r"in $1{,}000$ classes", width=6.0, color=C.NEURAL).move_to([-3.4, 1.7, 0])
        vals = [26.2, 15.3]
        bars = LiveBars([0, 0], max_value=30, height=3.4, bar_width=1.2, gap=1.4, colors=[GREY_B, GPUC],
                        show_values=True, digits=1, value_font=30,
                        labels=[r"second place", r"AlexNet"], label_font=24)
        bars.place(base_y=-2.4, x=3.6)
        bt = label(r"ILSVRC 2012: \ top-5 error, \%", font_size=24, color=GREY_A).move_to([3.6, 2.6, 0])
        who = label(r"Alex Krizhevsky, \ Ilya Sutskever, \ Geoffrey Hinton \ (Toronto)", font_size=22, color=GPUC)
        who.next_to(bt, DOWN, buff=0.2)
        # the contest: one photograph, five guesses, right if the true class is among them
        photo = RoundedRectangle(width=1.9, height=1.9, corner_radius=0.08, stroke_color=GREY_B, fill_color=GREY_D,
                                 fill_opacity=0.5).move_to([-5.1, -1.3, 0])
        pl = label(r"a test image", font_size=18, color=GREY_B).next_to(photo, DOWN, buff=0.1)
        guesses = VGroup(*[data_text(t, font_size=20, color=(GPUC if k == 2 else GREY_A))
                           for k, t in enumerate(["1. tiger cat", "2. tabby cat", "3. Egyptian cat", "4. lynx",
                                                  "5. tiger"])]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        guesses.next_to(photo, RIGHT, buff=0.4)
        ok = SurroundingRectangle(guesses[2], color=GPUC, buff=0.06)
        il = note(r"illustrative: \ right if the true class is among five guesses")
        il.next_to(VGroup(photo, pl, guesses), DOWN, buff=0.2).align_to(photo, LEFT)
        # a cat, drawn as an icon inside the photo frame (no real photograph)
        c0 = photo.get_center() + DOWN * 0.12
        head = Circle(radius=0.5, stroke_color=GREY_A, stroke_width=2, fill_color=C.HOT, fill_opacity=0.35).move_to(c0)
        ears = VGroup(*[Polygon(c0 + np.array([sx * 0.42, 0.18, 0]), c0 + np.array([sx * 0.38, 0.72, 0]),
                                c0 + np.array([sx * 0.08, 0.45, 0]), stroke_color=GREY_A, stroke_width=2,
                                fill_color=C.HOT, fill_opacity=0.35) for sx in (-1, 1)])
        eyes = VGroup(*[Dot(c0 + np.array([sx * 0.2, 0.1, 0]), radius=0.05, color=WHITE) for sx in (-1, 1)])
        whisk = VGroup(*[Line(c0 + np.array([sx * 0.12, -0.12 + dy, 0]), c0 + np.array([sx * 0.7, -0.08 + 2 * dy, 0]),
                              stroke_width=1.2, color=GREY_A) for sx in (-1, 1) for dy in (-0.06, 0.06)])
        cat = VGroup(ears, head, eyes, whisk)
        cite_ = cite(r"Krizhevsky, Sutskever \& Hinton (2012)", corner=DL)
        with self.voiceover(
            "By 2012 the ingredients were in place. <bookmark mark='a'/> In 2009 Fei-Fei Li's group had published "
            "ImageNet, millions of labelled photographs, and from 2010 there was a yearly contest: a model sees an "
            "image and names it, out of a thousand classes, with five guesses. <bookmark mark='b'/> In 2012 a "
            "network from Geoffrey Hinton's lab in Toronto, built by Alex Krizhevsky and Ilya Sutskever, "
            "<bookmark mark='c'/> missed on 15.3 percent of the test images. The next best entry missed on 26.2 "
            "percent. Nobody had seen a gap like that."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(photo), FadeIn(cat), FadeIn(pl), LaggedStart(*[FadeIn(g_) for g_ in guesses],
                                                                          lag_ratio=0.2))
            self.play(Create(ok), FadeIn(il))
            vo.wait_until("b")
            self.play(FadeIn(bt), FadeIn(who), FadeIn(cite_))
            vo.wait_until("c")
            self.add(bars)
            self.play(*bars.to(vals), run_time=1.5)
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stream(self, y, color) -> VGroup:
        sizes = [(0.5, 1.5), (0.45, 1.2), (0.4, 0.95), (0.4, 0.95), (0.4, 0.8), (0.25, 1.3), (0.25, 1.3)]
        boxes = VGroup(*[Prism(dimensions=[w, h, h], fill_color=color, fill_opacity=0.35, stroke_width=0.8)
                         .scale(0.9) for w, h in sizes])
        boxes.arrange(RIGHT, buff=0.55).move_to([0.2, y, 0])
        return boxes

    def two_gpus(self):
        top = self.stream(1.1, GPUC)
        bot = self.stream(-1.3, C.NEURAL)
        names = VGroup(label(r"GPU 1", font_size=24, color=GPUC).next_to(top, LEFT, buff=0.4),
                       label(r"GPU 2", font_size=24, color=C.NEURAL).next_to(bot, LEFT, buff=0.4))
        inp = Square(1.3, stroke_color=GREY_B, fill_color=GREY_D, fill_opacity=0.4).move_to([-5.6, -0.1, 0])
        il = label(r"image", font_size=20, color=GREY_B).next_to(inp, DOWN, buff=0.1)
        same = VGroup(*[Arrow(top[i].get_right(), top[i + 1].get_left(), buff=0.05, stroke_width=2, color=GPUC,
                              max_tip_length_to_length_ratio=0.25) for i in range(6)],
                      *[Arrow(bot[i].get_right(), bot[i + 1].get_left(), buff=0.05, stroke_width=2, color=C.NEURAL,
                              max_tip_length_to_length_ratio=0.25) for i in range(6)])
        cross = VGroup(*[Line(top[i].get_right(), bot[i + 1].get_left(), stroke_width=2, color=FLOPC)
                         for i in (1, 4, 5)],
                       *[Line(bot[i].get_right(), top[i + 1].get_left(), stroke_width=2, color=FLOPC) for i in (1, 4, 5)])
        cl = label(r"the only places the two cards talk", font_size=22, color=FLOPC).move_to([0.6, -0.1, 0])
        cl.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.06)
        facts = VGroup(label(r"$60$ million parameters, \ $650{,}000$ neurons", font_size=22, color=GREY_A),
                       label(r"two GeForce GTX 580 cards, \ $3$ GB each", font_size=22, color=GREY_A),
                       label(rf"$90$ passes over the data: \ ${ALEXNET_DAYS[0]}$ to ${ALEXNET_DAYS[1]}$ days",
                             font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.3)
        if facts.width > 13.4:
            facts.width = 13.4
        tag = schematic_tag(corner=UR)
        with self.voiceover(
            "What made it possible was two gaming graphics cards. <bookmark mark='a'/> The network had sixty "
            "million parameters, and one GeForce GTX 580, with three gigabytes of memory, couldn't hold it while "
            "training. So Krizhevsky split it: half the filters of each layer on one card, half on the other. "
            "<bookmark mark='b'/> The two halves exchange their results only at a few layers, to keep the traffic "
            "between the cards small. <bookmark mark='c'/> He wrote the convolutions himself, in CUDA, in a library "
            "called cuda-convnet. Training took five to six days, for ninety passes over the 1.2 million images."
        ) as vo:
            self.play(FadeIn(inp), FadeIn(il), FadeIn(names), FadeIn(top, lag_ratio=0.1), FadeIn(bot, lag_ratio=0.1),
                      FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in same], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in cross], lag_ratio=0.1), FadeIn(cl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in facts], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def arithmetic(self):
        mm = load("matmul")
        mt = load("matmul_mt")
        r1 = max(r[1] for r in mm["np_float32"])
        rN = max(r[1] for r in mt["np_float32"])
        days = sum(ALEXNET_DAYS) / 2
        avail = 2 * GPUS["GTX 580"]["fp32"] * days * 86400
        use = ALEXNET_FLOP / avail
        d1, dN = ALEXNET_FLOP / r1 / 86400, ALEXNET_FLOP / rN / 86400
        colors = {r"F": FLOPC}
        prod = 1.2e6 * 90 * 0.75e9 * 2 * 3
        rows = [
            cmath(r"1.2 \times 10^{6}", r"\times", r"90", r"\times", r"0.75 \times 10^{9}", r"\times", r"2", r"\times",
                  r"3", font_size=34),
            cmath(r"\approx", rf"{prod / 1e17:.1f} \times 10^{{17}}\ \text{{FLOP}}", font_size=40),
        ]
        rows[1][1].set_color(FLOPC)
        whys = [why(r"images $\times$ passes $\times$ multiply-adds per image $\times$ 2 FLOP $\times$ (forward $+$ "
                    r"backward)"), why(r"the published estimate: \ $4.7 \times 10^{17}$ \ (OpenAI 2018; Epoch AI)")]
        step = ladder(self, rows, whys, keep=2, top=2.9, x=-1.2, align_index=None, buff=0.55, edge=6.8)
        cap = label(rf"two GTX 580s for ${days:g}$ days at their peak: \ "
                    rf"${avail / 1e18:.1f} \times 10^{{18}}$ FLOP \ $\Rightarrow$ \ ${100 * use:.0f}\%$ of it used",
                    font_size=26, color=GPUC).move_to([0, 0.0, 0])
        here = VGroup(
            label(rf"this computer, \ one core \ (${r1 / 1e9:.0f}$ GFLOP/s, measured): \ ${d1:.0f}$ days", font_size=26,
                  color=CPUC),
            label(rf"all ${int(mt['threads'])}$ cores \ (${rN / 1e9:.0f}$ GFLOP/s): \ ${dN:.0f}$ days", font_size=26,
                  color=CPUC) if rN >= 1.5 * r1 else
            label(rf"all ${int(mt['threads'])}$ cores: \ no faster than one, \ shared with other jobs", font_size=26,
                  color=CPUC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.6, 0])
        tag = note(r"computed: \ matrix products on this computer, \ at its best measured speed").to_corner(DR,
                                                                                                         buff=0.2)
        cards = VGroup(*[RoundedRectangle(width=0.6, height=0.36, corner_radius=0.05, stroke_color=GPUC,
                                          fill_color=GPUC, fill_opacity=0.5) for _ in range(2)]).arrange(RIGHT, buff=0.1)
        cpu = RoundedRectangle(width=0.9, height=0.9, corner_radius=0.08, stroke_color=CPUC, fill_color=CPUC,
                               fill_opacity=0.3)
        cap.shift(RIGHT * 0.6)
        here.shift(RIGHT * 0.6)
        cards.next_to(cap, LEFT, buff=0.35)
        cpu.next_to(here, LEFT, buff=0.35)
        faster = "faster" if dN < days else "slower"
        if rN >= 1.5 * r1:
            tail = (f", and all {int(mt['threads'])} cores together about {dN:.0f}: {faster} than two graphics cards "
                    "from 2010, if every core did nothing but matrix products.")
        else:
            tail = (f". All {int(mt['threads'])} cores together should do better, but other jobs were using them when "
                    "we measured, and together they were no faster than one.")
        with self.voiceover(
            "How much arithmetic was that? <bookmark mark='a'/> About 1.2 million images, times ninety passes, "
            "times three quarters of a billion multiply-adds per image, times two operations each, times three, "
            f"for the backward pass: <bookmark mark='b'/> about {prod / 1e17:.1f} times ten to the seventeen "
            "floating-point operations; the published estimate is 4.7. <bookmark mark='c'/> The two cards could do "
            f"about {avail / 1e18:.1f} times ten to the eighteen in five "
            f"and a half days, so the network kept them about {100 * use:.0f} percent busy. <bookmark mark='d'/> "
            "On the computer rendering this video, at the best speed we measured, one core would take "
            f"about {d1:.0f} days" + tail
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(cards), FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeIn(cpu), FadeIn(here[0]), FadeIn(tag))
            self.play(FadeIn(here[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def aftermath(self):
        items = [
            (2014, r"cuDNN", r"NVIDIA's library of deep-learning kernels: \ convolutions written once, well, for "
             r"everyone", GPUC),
            (2016, r"DGX-1", r"NVIDIA's eight-GPU server; \ Jensen Huang delivers the first one to OpenAI", GPUC),
            (2018, r"Amodei \& Hernandez, \ \textit{AI and Compute}",
             rf"the largest training runs doubled every ${AI_AND_COMPUTE['doubling_months']}$ months from 2012: "
             rf"\ $300{{,}}000\times$ in six years", FLOPC),
            (2020, r"Sara Hooker, \ \textit{The Hardware Lottery}", r"ideas win when they suit the hardware of their "
             r"day; \ neural networks drew a lucky ticket in games", C.NEURAL),
        ]
        cards = VGroup(*[history_card(y, w, t, width=6.4, color=c, font_size=23) for y, w, t, c in items])
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.45)).move_to(DOWN * 0.15)
        head = label(r"After AlexNet", font_size=36, color=GPUC).to_edge(UP, buff=0.45)
        with self.voiceover(
            "After 2012 the field moved onto GPUs. <bookmark mark='a'/> In 2014 NVIDIA released cuDNN, a library of "
            "deep-learning kernels, so researchers no longer had to write their own. <bookmark mark='b'/> In 2016 "
            "it built a server around eight GPUs, the DGX-1, and Jensen Huang delivered the first one to OpenAI "
            "himself. <bookmark mark='c'/> In 2018 Dario Amodei and Danny Hernandez measured the trend: from AlexNet "
            "on, the compute in the largest training runs had doubled every 3.4 months, three hundred thousand "
            "times in six years. <bookmark mark='d'/> And in 2020 Sara Hooker gave the history a name: the hardware "
            "lottery. Ideas succeed when they suit the hardware of their day, and neural networks, all multiply-adds, "
            "had drawn a winning ticket, made for video games."
        ) as vo:
            ghosts = cards.copy().set_opacity(0.12)  # the four milestones to come, faint, then each in turn
            self.play(FadeIn(head), FadeIn(ghosts, lag_ratio=0.1), run_time=1.2)
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeOut(ghosts[k]), FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
