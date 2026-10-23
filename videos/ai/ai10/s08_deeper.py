from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (CNN, FMAP, GRADC, HAND, HIST, KERNEL, PART, box_label, load)
from videos.ai.ai10.specs import HUMAN_TOP5, ILSVRC, VGG_2014


class Deeper(VoiceoverScene):
    def construct(self):
        self.card()
        self.years()
        self.vgg()
        self.inception()
        self.resnet()

    def card(self):
        card = chapter_card(7, r"Deeper: VGG, Inception, ResNet", r"If depth helps, why not a hundred layers?",
                            lit=(2012, 2015), part=PART)
        with self.voiceover("Chapter seven. Deeper: VGG, Inception, ResNet."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def years(self):
        bars = VGroup()
        H = 4.6
        for k, (y, team, err, how) in enumerate(ILSVRC):
            h = H * err / 30
            c = HAND if y < 2012 else CNN
            b = Rectangle(width=1.0, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-5.6 + 1.45 * k, -2.5 + h / 2, 0])
            v = MathTex(rf"{err:g}\%", font_size=26, color=c).next_to(b, UP, buff=0.08)
            v.add_background_rectangle(color=config.background_color, opacity=1.0, buff=0.05)
            yl = MathTex(str(y), font_size=22, color=GREY_B).next_to(b, DOWN, buff=0.1)
            tl = label(team, font_size=16, color=GREY_A).next_to(yl, DOWN, buff=0.06)
            if tl.width > 1.4:
                tl.width = 1.4
            bars.add(VGroup(b, v, yl, tl))
        base = Line([-6.3, -2.5, 0], [5.1, -2.5, 0], color=GREY_C, stroke_width=1.5)
        hy = -2.5 + H * HUMAN_TOP5 / 30
        human = DashedLine([-6.3, hy, 0], [5.1, hy, 0], color=HIST, stroke_width=2.5).set_z_index(-1)
        hl = label(rf"one trained person: \ ${HUMAN_TOP5}\%$", font_size=22, color=HIST).next_to(human, UP, buff=0.08)
        hl.align_to(human, RIGHT)
        head = label(r"ILSVRC: \ the winning top-5 error, \ year by year", font_size=30).to_edge(UP, buff=0.4)
        cite_ = cite(r"Russakovsky et al.\ (2015); \ He et al.\ (2015); \ Hu et al.\ (2017); \ Recht et al.\ (2019)",
                     corner=DR)
        recht = label(r"2019, \ Recht et al.: \ a fresh test set made the same way; \\ every model $11$--$14$ "
                      r"points less accurate, \ the ranking nearly unchanged", font_size=22, color=HIST).move_to([2.6, 1.6, 0])
        keep_in_frame(recht)
        with self.voiceover(
            "After 2012 the contest became a race to go deeper. <bookmark mark='a'/> The winning error, year by "
            f"year: {ILSVRC[2][2]} percent for AlexNet's eight layers; {ILSVRC[3][2]} in 2013; {ILSVRC[4][2]} in "
            f"2014, with twenty-two layers; {ILSVRC[5][2]} in 2015, with a hundred and fifty-two. "
            "<bookmark mark='b'/> In 2014 Andrej Karpathy trained himself on the task and labelled test images by "
            f"hand: he missed {HUMAN_TOP5} percent. The networks passed him in 2015. <bookmark mark='c'/> By the "
            f"contest's last year, 2017, the winner missed {ILSVRC[-1][2]} percent. <bookmark mark='d'/> When "
            "Benjamin Recht and colleagues later built a fresh test set the same way, every model lost eleven to "
            "fourteen points of accuracy, though the ranking barely changed. Part 31 asks what benchmarks can tell us."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(cite_))
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars[:3]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars[3:6]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(human), FadeIn(hl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars[6:]], lag_ratio=0.5))
            vo.wait_until("d")
            self.play(FadeIn(recht, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vgg(self):
        a = load("alexnet")
        S = a["vgg16_sum"]
        colors = {r"18C^2": KERNEL, r"25C^2": GREY_B, r"27C^2": KERNEL, r"49C^2": GREY_B}
        rows = [
            cmath(r"\text{two } 3\times 3", r"=", r"1 + 2 + 2 = 5", font_size=36),
            cmath(r"\text{weights}", r"=", r"2 \cdot 9 C^2", r"=", r"18C^2", r"<", r"25C^2", colors=colors,
                  font_size=36),
            cmath(r"\text{three } 3\times 3", r"=", r"7 \times 7:\ ", r"27C^2", r"<", r"49C^2", colors=colors,
                  font_size=36),
        ]
        whys = [why(r"the receptive-field rule, \ stride $1$"), why(r"$C$ channels in, $C$ out"),
                why(r"and two more nonlinearities in between")]
        step = ladder(self, rows, whys, keep=3, top=0.9, x=-0.8, align_index=1, edge=6.8)
        hc = history_card(2014, r"Karen Simonyan \& Andrew Zisserman, \ Oxford (VGG)",
                          rf"only $3 \times 3$ convolutions, \ $16$ or $19$ layers; \ second in 2014 at "
                          rf"${VGG_2014}\%$", width=5.6, color=HIST).to_corner(UL, buff=0.35)
        tot = label(rf"VGG-16, \ counted from its layer list: \ ${S['params'] / 1e6:.0f}$ million weights, \ "
                    rf"${S['macs'] / 1e9:.1f}$ billion multiply-adds per image", font_size=24, color=CNN)
        tot.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In 2014 Karen Simonyan and Andrew Zisserman at Oxford asked how far depth alone would go, and built "
            "networks of sixteen and nineteen layers out of nothing but three-by-three convolutions. "
            "<bookmark mark='a'/> Why so small? Two three-by-three layers see five by five pixels, by the rule of "
            "Chapter 3. <bookmark mark='b'/> With C channels in and out, they cost eighteen C squared weights, "
            "against twenty-five C squared for one five-by-five layer. <bookmark mark='c'/> Three of them see "
            "seven by seven, for twenty-seven against forty-nine, and add two more nonlinearities in between. "
            f"<bookmark mark='d'/> VGG-16 came second in 2014. It was big: {S['params'] / 1e6:.0f} million weights "
            f"and {S['macs'] / 1e9:.1f} billion multiply-adds per image, by our count from its layer list."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(tot, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inception(self):
        inp = box_label(r"the previous layer", GREY_B, font_size=22).move_to([0, 2.5, 0])
        branches = VGroup(
            VGroup(box_label(r"$1 \times 1$", KERNEL, font_size=22)),
            VGroup(box_label(r"$1 \times 1$", FMAP, font_size=22), box_label(r"$3 \times 3$", KERNEL, font_size=22)),
            VGroup(box_label(r"$1 \times 1$", FMAP, font_size=22), box_label(r"$5 \times 5$", KERNEL, font_size=22)),
            VGroup(box_label(r"$3 \times 3$ pool", GREY_B, font_size=22), box_label(r"$1 \times 1$", FMAP,
                                                                                     font_size=22)),
        )
        for b in branches:
            b.arrange(DOWN, buff=0.45)
        branches.arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, 0.4, 0])
        cat = box_label(r"stacked side by side", GREY_B, font_size=22).move_to([0, -1.7, 0])
        arrows = VGroup()
        for b in branches:
            arrows.add(Arrow(inp.get_bottom(), b[0].get_top(), buff=0.08, color=GREY_C, stroke_width=2,
                             max_tip_length_to_length_ratio=0.1))
            if len(b) == 2:
                arrows.add(Arrow(b[0].get_bottom(), b[1].get_top(), buff=0.05, color=GREY_C, stroke_width=2,
                                 max_tip_length_to_length_ratio=0.2))
            arrows.add(Arrow(b[-1].get_bottom(), cat.get_top(), buff=0.08, color=GREY_C, stroke_width=2,
                             max_tip_length_to_length_ratio=0.1))
        red = VGroup(*[b[0] for b in branches[1:3]], branches[3][1])
        rl = label(r"$1 \times 1$ convolutions: \\ fewer channels first", font_size=22, color=FMAP)
        rl.next_to(branches, LEFT, buff=0.4)
        keep_in_frame(rl)
        hc = history_card(2014, r"Christian Szegedy and colleagues, \ Google: \ GoogLeNet",
                          rf"$22$ layers of such modules; \ the 2014 winner at ${ILSVRC[4][2]}\%$; \ about a twelfth "
                          r"of AlexNet's weights", width=4.8, color=HIST).to_corner(DL, buff=0.3)
        tag = note(r"schematic: \ one Inception module").to_corner(UR, buff=0.3)
        with self.voiceover(
            "The winner of 2014 went another way. <bookmark mark='a'/> Christian Szegedy's team at Google built "
            "GoogLeNet from Inception modules: look at the previous layer through several windows at once, and "
            "stack the results side by side. <bookmark mark='b'/> What made it affordable: a one-by-one "
            "convolution in front of each big one, to cut the number of channels before the expensive step. "
            "<bookmark mark='c'/> Twenty-two layers, the best error of the year, and, by its authors' count, a "
            "twelfth of AlexNet's weights. Deeper didn't have to mean bigger."
        ) as vo:
            self.play(FadeIn(inp), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in branches], lag_ratio=0.2), Create(arrows), FadeIn(cat))
            vo.wait_until("b")
            self.play(*[Indicate(r, color=FMAP) for r in red], FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def resnet(self):
        hc = history_card(2015, r"Kaiming He, Xiangyu Zhang, Shaoqing Ren \& Jian Sun, \ Microsoft Research",
                          rf"residual networks: \ $152$ layers; \ the 2015 winner at ${ILSVRC[5][2]}\%$",
                          width=5.6, color=HIST).to_corner(UL, buff=0.35)
        prob = label(r"a plain $56$-layer network trained worse than a $20$-layer one \\ "
                     r"(CIFAR-10, \ He et al.): \ not overfitting, \ worse on the training data too", font_size=22,
                     color=GREY_A).next_to(hc, DOWN, buff=0.35).align_to(hc, LEFT)
        x_in = Dot([3.0, 2.3, 0], radius=0.07)
        xl = MathTex(r"x", font_size=34).next_to(x_in, UP, buff=0.1)
        F1 = box_label(r"conv, \ norm, \ ReLU", FMAP, font_size=20).move_to([3.0, 1.2, 0])
        F2 = box_label(r"conv, \ norm", FMAP, font_size=20).move_to([3.0, 0.0, 0])
        plus = MathTex(r"\oplus", font_size=48).move_to([3.0, -1.1, 0])
        out = MathTex(r"y = F(x) + x", font_size=34).move_to([3.0, -1.9, 0])
        a1 = Arrow(x_in.get_center(), F1.get_top(), buff=0.06, stroke_width=2.5, color=GREY_B)
        a2 = Arrow(F1.get_bottom(), F2.get_top(), buff=0.06, stroke_width=2.5, color=GREY_B)
        a3 = Arrow(F2.get_bottom(), plus.get_top(), buff=0.06, stroke_width=2.5, color=GREY_B)
        xr = max(F1.get_right()[0], F2.get_right()[0]) + 0.6
        p0, p3 = x_in.get_center(), plus.get_right()
        skip = VGroup(Line(p0, [xr, p0[1], 0], color=KERNEL, stroke_width=3),
                      Line([xr, p0[1], 0], [xr, p3[1], 0], color=KERNEL, stroke_width=3),
                      Arrow([xr, p3[1], 0], p3, buff=0.04, color=KERNEL, stroke_width=3,
                            max_tip_length_to_length_ratio=0.3))
        sl = label(r"identity", font_size=22, color=KERNEL).next_to(skip[1], RIGHT, buff=0.12)
        der = cmath(r"\frac{\partial y}{\partial x}", r"=", r"I", r"+", r"\frac{\partial F}{\partial x}",
                    colors={r"I": KERNEL, r"\frac{\partial F}{\partial x}": FMAP}, font_size=40)
        der.move_to([-3.5, -1.3, 0])
        dl = label(r"a path the gradient can always take: \ Part 9", font_size=22, color=GRADC).next_to(der, DOWN,
                                                                                                     buff=0.3)
        bn = label(r"batch normalization (Ioffe \& Szegedy, 2015): \ each layer's inputs kept at mean 0, \ "
                   r"variance 1", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        hw = label(r"highway networks, May 2015: \ the same idea with gates, \ from the LSTM (Chapter 12)",
                   font_size=20, color=GREY_B).next_to(bn, UP, buff=0.12)
        with self.voiceover(
            "Then depth hit a wall. <bookmark mark='a'/> Kaiming He and his colleagues at Microsoft found a plain "
            "network of fifty-six layers doing worse than one of twenty, even on its own training data: not "
            "overfitting, just harder to train. Batch normalization, from Sergey Ioffe and Szegedy that year, which "
            "keeps each layer's inputs standardized, had helped, but not enough. <bookmark mark='b'/> Their fix: "
            "let each pair of layers learn only a correction F of x, added to its input. <bookmark mark='c'/> The "
            "block's derivative is the identity plus F's: a path along which the gradient always passes, however "
            "deep the stack, as Part 9 derived. <bookmark mark='d'/> A hundred and fifty-two layers won 2015 at "
            f"{ILSVRC[5][2]} percent. Months earlier, highway networks from Schmidhuber's lab had built the same "
            "path with gates, borrowed from the LSTM of Chapter 12."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(prob), FadeIn(bn))
            vo.wait_until("b")
            self.play(FadeIn(x_in), FadeIn(xl), GrowArrow(a1), FadeIn(F1), GrowArrow(a2), FadeIn(F2), GrowArrow(a3),
                      FadeIn(plus))
            self.play(Create(skip), FadeIn(sl), FadeIn(out))
            vo.wait_until("c")
            self.play(Write(der), FadeIn(dl))
            vo.wait_until("d")
            self.play(FadeIn(hw))
        self.wait(0.3)
        self.clear_scene()


_ = np
