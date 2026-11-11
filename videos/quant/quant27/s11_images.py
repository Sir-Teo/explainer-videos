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
        keys = VGroup(wrapped_label(r'Original 20-day chart pixels; open is proxied by the previous close.',12.0,23,GREY_A),wrapped_label(r'Selected test-prediction extremes, not representative or known-correct forecasts.',12.0,23,GREY_A),wrapped_label(r'32 by 60 binary pixels, moving average and quote-volume bars; display colour identifies the selected case.',12.0,23,GREY_A)).arrange(DOWN,aligned_edge=LEFT,buff=.12).to_edge(DOWN,buff=.3)
        with self.voiceover(
            "A chart-image representation converts recent history into pixels. <bookmark mark='a'/> This original uses a twenty-day window, high-low marks, moving averages and volume; its open is proxied by the previous close. That differs from observing every true opening price. <bookmark mark='b'/> Window scaling removes the absolute price level, while preserving selected relative geometry. <bookmark mark='c'/> The two displayed examples are selected for extreme network predictions in the test sample. They are neither representative random examples nor proof that those predictions were correct."
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
        whys = [why('Convolution shares local filters. Translation equivariance depends on boundary conventions; pooling and the head need not make the full predictor shift invariant.'),
                why(r"cross-entropy on $y_n = 1$ if the next five days' return is positive; the network outputs a "
                    r"probability, and the portfolio sorts on it")]
        step = ladder(self, rows, whys, keep=2, top=0.4, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The House uses a small two-block convolutional classifier. <bookmark mark='a'/> Shared filters scan local pixel patterns, followed by pooling, nonlinearities and a linear probability head. <bookmark mark='b'/> Convolution is translation equivariant under suitable boundary conventions, but padding, pooling and the head can make pattern position matter. The complete classifier is not necessarily shift invariant. <bookmark mark='c'/> Cross-entropy trains a five-day direction target. Classification probability, ranking quality and net trading value are distinct evaluation questions."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b_) for b_ in chain], lag_ratio=0.15), Create(arrows), run_time=2)
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def paper(self):
        cards = VGroup(
            desk_question(r"not momentum, not reversal", 'Author-reported stock-sample comparison with selected hand-crafted benchmarks; not replicated here.', width=12.2, font_size=29),
            desk_question(r"more profitable", "Author-reported portfolio results under the authors' sample and implementation assumptions.", width=12.2, font_size=29),
            desk_question(r"context independent", 'The paper studies transfer across selected horizons and markets; this is not a universal transfer guarantee.', width=12.2, font_size=29),
        ).arrange(DOWN, buff=0.22).move_to(UP * 0.2)
        src = note(r"Jiang, Kelly and Xiu (2023), ``(Re-)Imag(in)ing Price Trends'', \textit{Journal of Finance} 78(6): "
                   r"trained on U.S. stocks, 1993--2000; tested 2001--2019", font_size=15, color=GREY_C).to_edge(DOWN,
                                                                                                       buff=0.3)
        with self.voiceover(
            "Jiang, Kelly and Xiu report evidence from stock-chart experiments. <bookmark mark='a'/> Their learned chart signals differ from selected hand-crafted trend benchmarks. <bookmark mark='b'/> Their paper reports portfolio improvements under its own sample, portfolio and implementation choices. <bookmark mark='c'/> It also studies transfer across horizons and markets. These are the authors' findings, rather than a universal chart-predictability result or a replication by this much smaller coin network."
        ) as vo:
            self.play(FadeIn(src),FadeIn(cards[0]))
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def result(self, im):
        hx = [-3.4, 1.4, 4.4]
        head = VGroup(label(r"coins, test year 2020", font_size=18, color=GREY_B), label(r"CNN on charts", font_size=20, color=NET),
                      label(r"20-day momentum", font_size=20, color=MOM))
        data = [(r"up or down right, 2020", rf"{100 * im['acc']:.1f}\%", rf"{100 * im['acc_mom']:.1f}\%"),
                ('test-majority prevalence (hindsight)', rf"{100 * im['base']:.1f}\%", rf"{100 * im['base']:.1f}\%"),
                (r"quintile long-short Sharpe, 5-day", rf"{im['sr_cnn']:.2f}", rf"{im['sr_mom']:.2f}"),
                (r"rank correlation with momentum", rf"{im['corr_mom']:.2f}", r"1")]
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(a, font_size=18, color=GREY_A), MathTex(b, font_size=26),
                                                 MathTex(c, font_size=26)) for a, b, c in data]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.65 * j, 0])
            row[0].align_to(np.array([hx[0] - 3.0, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label(rf"Original {comma(im['n_train'])} overlapping training images and {comma(im['n_test'])} test images; three seeds averaged. Weekly sampled five-day gross payoffs omit costs and borrow. Majority baseline uses test-label prevalence.",12.0,23,GREY_A).to_edge(DOWN,buff=.35)
        with self.voiceover(
            f"The saved crypto classifier has test direction accuracy {100*im['acc']:.2f} percent. <bookmark mark='a'/> The majority-class diagnostic is {100*im['base']:.2f} percent, calculated from test-label prevalence; it is a hindsight benchmark, not a training-locked trading rule. <bookmark mark='b'/> Gross portfolio Sharpe is {im['sr_cnn']:.3f} for the CNN and {im['sr_mom']:.3f} for momentum, with rank correlation {im['corr_mom']:.3f}. Five-day targets are sampled weekly. Costs, borrow, overlapping training windows and limited history constrain interpretation. The comparison does not identify a single missing pattern as the cause."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def hunger(self, im):
        n_par = 16*15+16+2*16+32*16*15+32+2*32+32*8*60+1
        rows = VGroup(
            MathTex(rf"\text{{weights}}:\ {comma(n_par)}", font_size=30, color=NET),
            MathTex(rf"\text{{training images}}:\ {comma(im['n_train'])}\ \ (\text{{and they overlap}})", font_size=30,
                    color=COIN),
            MathTex(r"\text{Jiang, Kelly and Xiu: every U.S. stock, every week, eight years}", font_size=30,
                    color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.8)
        lesson = wrapped_label('Overlapping samples, model priors, optimisation and target choices complicate comparison. Limited data is a plausible limitation, not an isolated causal explanation.', 11.0, 25,
                               QC.HOUSE).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            f"Consider sample size and inductive bias without overclaiming causation. <bookmark mark='a'/> Counting convolution, affine batch-normalisation and linear-head parameters gives {n_par} trainable scalars. The original uses {im['n_train']} training images, with overlapping windows. <bookmark mark='b'/> The cited stock study has a different and much larger design. <bookmark mark='c'/> Model priors, optimisation, target definition, sample chronology and trading assumptions all differ. These outputs alone do not identify insufficient data as the unique cause, or prove that a simple rule always wins."
        ) as vo:
            self.add(rows[0],rows[1])
            vo.wait_until("a")
            self.wait(.1)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q=ask(r"Shared convolutional filters can be translation equivariant. Why is the full chart classifier not necessarily shift invariant? Give a financial pattern whose age within the window should matter.")
        with self.voiceover("Pause and predict. Distinguish local convolutional equivariance from invariance of the complete chart classifier. Give a pattern whose age within the window should matter for a forecast."):
            self.play(FadeIn(q))
        self.clear_scene()
