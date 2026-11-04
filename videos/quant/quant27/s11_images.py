from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MOM, NET, PART, TREE, ask, comma, fit_right, load


def pixels(img, cell=0.075, color=WHITE) -> VGroup:
    """A black-and-white chart image as squares (only the lit pixels), inside its frame."""
    img = np.asarray(img)
    H, W = img.shape
    frame = Rectangle(width=W * cell, height=H * cell, stroke_color=GREY_C, stroke_width=1.5, fill_color=BLACK,
                      fill_opacity=1)
    cols = VGroup()
    for j in range(W):
        col = VGroup()
        for i in range(H):
            if img[i, j] > 0.5:
                col.add(Square(side_length=cell, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
                    frame.get_corner(UL) + np.array([(j + 0.5) * cell, -(i + 0.5) * cell, 0])))
        cols.add(col)
    return VGroup(frame, cols)


class Images(VoiceoverScene):
    def construct(self):
        im = load("images")
        self.card()
        self.picture(im)
        self.network()
        self.paper()
        self.result(im)
        self.hunger(im)
        self.question()

    def card(self):
        c = chapter_card(10, r"Images of prices", r"Can a network that looks at charts see what chartists claim to?",
                         part=PART)
        with self.voiceover("Chapter ten. Technical analysts have looked at price charts for a century. What happens "
                            "when a network built to see does the looking?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def picture(self, im):
        up, dn = pixels(im["example_up"], color=GOOD), pixels(im["example_down"], color=BAD)
        pics = VGroup(up, dn).arrange(RIGHT, buff=0.8).move_to(UP * 0.5)
        caps = VGroup(label(r"the CNN's most confident `up'", font_size=18, color=GOOD).next_to(up, UP, buff=0.15),
                      label(r"its most confident `down'", font_size=18, color=BAD).next_to(dn, UP, buff=0.15))
        keys = VGroup(
            label(r"each day: three pixel columns, open tick, high--low bar, close tick", font_size=18, color=GREY_A),
            label(r"the line: the 20-day moving average; the bottom fifth: volume", font_size=18, color=GREY_A),
            label(r"32 by 60 pixels, black and white, scaled to the window's own range", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 2023 Jingwen Jiang, Bryan Kelly and Dacheng Xiu turned every stock's recent history into a picture. "
            "<bookmark mark='a'/> Each day is three columns of pixels: a tick for the open, a bar from the low to the "
            "high, a tick for the close. A moving average runs through it, and volume sits along the bottom. "
            "<bookmark mark='b'/> The picture is scaled to its own window, so a network sees the shape of the last "
            "twenty days and nothing about the level. <bookmark mark='c'/> These two are from the House's version, "
            "built on coins: the charts its network was most sure would rise, and most sure would fall."
        ) as vo:
            self.play(FadeIn(up[0]), FadeIn(caps[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in up[1]], lag_ratio=0.03, run_time=3), FadeIn(keys[0]))
            vo.wait_until("b")
            self.play(FadeIn(keys[1:]))
            vo.wait_until("c")
            self.play(FadeIn(dn), FadeIn(caps[1]))
        self.wait(0.4)
        self.clear_scene()

    def network(self):
        boxes = []
        spec = [(r"image\\$32 \times 60$", GREY_B, 1.1), (r"conv $5 \times 3$\\16 maps", NET, 1.3),
                (r"max-pool\\$2 \times 1$", NET, 1.0), (r"conv $5 \times 3$\\32 maps", NET, 1.3),
                (r"max-pool\\$2 \times 1$", NET, 1.0), (r"linear\\dropout", TREE, 1.0), (r"$\Pr(\text{up})$", GOOD, 1.0)]
        for txt, col, h in spec:
            b = RoundedRectangle(width=1.45, height=h, corner_radius=0.1, stroke_color=col, stroke_width=2,
                                 fill_color=col, fill_opacity=0.15)
            t_ = Tex(txt, font_size=20).move_to(b)
            boxes.append(VGroup(b, t_))
        chain = VGroup(*boxes).arrange(RIGHT, buff=0.35).move_to(UP * 1.9)
        arrows = VGroup(*[Arrow(chain[k].get_right(), chain[k + 1].get_left(), buff=0.05, stroke_width=2,
                                max_tip_length_to_length_ratio=0.3, color=GREY_B) for k in range(len(chain) - 1)])
        rows = [cmath(r"(K * x)_{ij}", r"=", r"\textstyle\sum_{a, b} K_{ab}\, x_{i + a,\, j + b}", font_size=30,
                      colors={r"(K * x)_{ij}": NET}),
                cmath(r"\mathcal L", r"=", r"-\textstyle\sum_n \big[y_n \log p_n + (1 - y_n)\log(1 - p_n)\big]",
                      font_size=30, colors={r"\mathcal L": HURDLE})]
        whys = [why(r"a convolution slides one small filter over the whole image: the same pattern is detected wherever "
                    r"it appears (translation equivariance), with few weights"),
                why(r"cross-entropy on $y_n = 1$ if the next five days' return is positive; the network outputs a "
                    r"probability, and the portfolio sorts on it")]
        step = ladder(self, rows, whys, keep=2, top=0.4, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The network is a small convolutional one, like the paper's. <bookmark mark='a'/> A filter five pixels "
            "tall and three wide slides over the whole image, so a pattern is detected wherever in the window it "
            "appears; sixteen such filters, then a pooling step that keeps the strongest response in each pair of "
            "rows; then thirty-two more, and a linear layer to a probability. <bookmark mark='b'/> The convolution "
            "is the reason this architecture conquered images: one filter, shared across every position, means few "
            "weights and no need to learn the same edge twice. <bookmark mark='c'/> It is trained by cross-entropy "
            "to say whether the next five days will be up."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in chain], lag_ratio=0.15), Create(arrows), run_time=2)
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def paper(self):
        cards = VGroup(
            desk_question(r"not momentum, not reversal", r"the patterns the network finds differ from the trend signals "
                          r"traders define by hand, and predict better", width=12.2, font_size=20),
            desk_question(r"more profitable", r"sorting stocks on the network's up-probability earns more than sorting on "
                          r"momentum or reversal, across the specifications the authors tried", width=12.2, font_size=20),
            desk_question(r"context independent", r"patterns learned on short windows work on longer ones, and patterns "
                          r"learned on American stocks work in other countries' markets", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.22).move_to(UP * 0.2)
        src = note(r"Jiang, Kelly and Xiu (2023), ``(Re-)Imag(in)ing Price Trends'', \textit{Journal of Finance} 78(6): "
                   r"trained on U.S. stocks, 1993--2000; tested 2001--2019", font_size=15, color=GREY_C).to_edge(DOWN,
                                                                                                       buff=0.3)
        with self.voiceover(
            "What the paper found, on American stocks. <bookmark mark='a'/> The patterns the network learns are not "
            "momentum or reversal, the signals traders define by hand, and they predict better than either. <bookmark "
            "mark='b'/> Sorting stocks on the network's probability of a rise makes more money than sorting on "
            "momentum. <bookmark mark='c'/> And the patterns travel: learned on short windows, they work on long ones; "
            "learned on American stocks, they work abroad. That is the strongest evidence yet that charts carry "
            "information. It was learned from every American stock over eight years."
        ) as vo:
            self.play(FadeIn(src))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def result(self, im):
        hx = [-3.4, 1.4, 4.4]
        head = VGroup(label(r"coins, test year 2020", font_size=18, color=GREY_B), label(r"CNN on charts", font_size=20, color=NET),
                      label(r"20-day momentum", font_size=20, color=MOM))
        data = [(r"up or down right, 2020", rf"{100 * im['acc']:.1f}\%", rf"{100 * im['acc_mom']:.1f}\%"),
                (r"always guessing the commoner outcome", rf"{100 * im['base']:.1f}\%", rf"{100 * im['base']:.1f}\%"),
                (r"quintile long-short Sharpe, 5-day", rf"{im['sr_cnn']:.2f}", rf"{im['sr_mom']:.2f}"),
                (r"rank correlation with momentum", rf"{im['corr_mom']:.2f}", r"1")]
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(a, font_size=18, color=GREY_A), MathTex(b, font_size=26),
                                                 MathTex(c, font_size=26)) for a, b, c in data]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.65 * j, 0])
            row[0].align_to(np.array([hx[0] - 3.0, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label(rf"trained on {comma(im['n_train'])} chart images from mid-2018 to mid-2019 (every day of each "
                             rf"week), tested on {comma(im['n_test'])} of 2020; three seeds averaged. In 2020 the market's "
                             r"own trend paid: momentum's Sharpe ratio is the year's, not a law", 12.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The House's coins. <bookmark mark='a'/> On 2020, the network called the direction of the next five days "
            "right forty-nine percent of the time; always guessing the commoner outcome was right fifty-two and a "
            "half. <bookmark mark='b'/> A portfolio sorted on its probability lost, a Sharpe ratio of minus a half, "
            "while plain twenty-day momentum, in a year when every coin trended, earned more than two and a half. The network's "
            "ranking barely agreed with momentum's. It had not found the year's one pattern."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def hunger(self, im):
        n_par = 16 * 15 + 16 + 32 * 16 * 15 + 32 + 32 * 8 * 60 + 1
        rows = VGroup(
            MathTex(rf"\text{{weights}}:\ {comma(n_par)}", font_size=30, color=NET),
            MathTex(rf"\text{{training images}}:\ {comma(im['n_train'])}\ \ (\text{{and they overlap}})", font_size=30,
                    color=COIN),
            MathTex(r"\text{Jiang, Kelly and Xiu: every U.S. stock, every week, eight years}", font_size=30,
                    color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.8)
        lesson = wrapped_label(r"a network that learns patterns from pixels needs many examples of each pattern; a "
                               r"hand-made signal like momentum needs none. With a small sample, the prior built into "
                               r"the simple rule is worth more than the flexibility of the network", 11.0, 20,
                               QC.HOUSE).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Why the difference? <bookmark mark='a'/> The House's network has about twenty-three thousand weights. It "
            "was trained on under seven thousand images, most of them overlapping days of the same few dozen coins. "
            "<bookmark mark='b'/> The paper's network saw every American stock, every week, for eight years. "
            "<bookmark mark='c'/> A network that learns patterns from pixels needs many examples of each pattern. A "
            "hand-made rule like momentum needs none: its prior is built in. On a small sample, that prior is worth "
            "more than all the flexibility in the world."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"the chart CNN is invariant to shifting a pattern left or right within the window. Is that a good "
                r"property for predicting returns? Give a pattern for which position should matter.")
        with self.voiceover(
            "Pause and predict. A convolutional network treats a pattern the same wherever it appears in the window. "
            "Is that a good property for predicting returns? Give a pattern whose position should matter."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
