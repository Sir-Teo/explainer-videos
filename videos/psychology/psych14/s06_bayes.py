from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


class Bayes(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.gaussians()
        self.algebra()
        self.shrinkage()
        self.worth()

    def card(self):
        card = chapter_card(5, r"Bayes for perception", r"What is the best possible guess from an ambiguous image?",
                            lit={1763: r"Bayes", 1867: r"Helmholtz"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter five. Bayes for perception."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rule(self):
        head = heading(r"Unconscious inference, \ written down")
        eq = MathTex(r"p(", r"\text{world}", r"\mid", r"\text{image}", r")", r"\;\propto\;", r"p(", r"\text{image}",
                     r"\mid", r"\text{world}", r")", r"\;\times\;", r"p(", r"\text{world}", r")", font_size=50)
        eq.move_to([0, 1.3, 0])
        post = VGroup(eq[0:5])
        like = VGroup(eq[6:11])
        prior = VGroup(eq[12:15])
        bl = Brace(post, DOWN, color=POST)
        bk = Brace(like, DOWN, color=LIKE)
        bp = Brace(prior, DOWN, color=PRIOR)
        tl = label(r"posterior", font_size=28, color=POST).next_to(bl, DOWN, buff=0.12)
        tk = label(r"likelihood", font_size=28, color=LIKE).next_to(bk, DOWN, buff=0.12)
        tp = label(r"prior", font_size=28, color=PRIOR).next_to(bp, DOWN, buff=0.12)
        rows = rows_of([
            (r"likelihood: \ how probable this image would be, \ if the world were so: \ optics and noise", LIKE),
            (r"prior: \ how probable the world is, \ before the image: \ light from above, \ rooms are rectangular", PRIOR),
            (r"posterior: \ the bet, \ with its uncertainty; \ the percept is a choice from it", POST),
        ], 12.4, 28, 0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Helmholtz's unconscious inference was a phrase. In the last forty years it has become a calculation. "
            "<bookmark mark='a'/> Bayes's rule, from Part 4, says the probability of a world, given the image, is "
            "proportional to the probability of the image, given that world, times the probability of that world in "
            "the first place. <bookmark mark='b'/> The likelihood is the physics: how probable this image would be if "
            "the world were so, given the optics of the eye and the noise in its receptors. <bookmark mark='c'/> The "
            "prior is what the visual system knows before it looks: that light usually comes from above, that rooms "
            "are usually rectangular, that most things are still or move slowly. <bookmark mark='d'/> The posterior "
            "is the bet: every possible world, weighted by how probable it is now. What you see is a choice made "
            "from it, usually the most probable world, or the average."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), run_time=2.0)
            vo.wait_until("b")
            self.play(GrowFromCenter(bk), FadeIn(tk), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(GrowFromCenter(bp), FadeIn(tp), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(GrowFromCenter(bl), FadeIn(tl), FadeIn(rows[2]))
        self.clear_scene()

    def gaussians(self):
        d = load("bayes")
        head = heading(r"A prior, \ a measurement, \ a posterior")
        A = axes([-4, 8], [0, 0.5], x_length=8.0, y_length=4.2, xticks=[-4, -2, 0, 2, 4, 6, 8], yticks=[0, 0.25, 0.5],
                 xlabel=r"the quantity: \ a size, \ a speed, \ a slant", ylabel=r"probability density",
                 center=[-2.2, -0.3, 0])
        ax = A.ax
        cp = curve(ax, d["x"], d["prior"], PRIOR, stroke_width=4)
        cl = curve(ax, d["x"], d["like"], LIKE, stroke_width=4)
        cq = curve(ax, d["x"], d["post"], POST, stroke_width=5)
        mark = DashedLine(ax.c2p(d["post_m"], 0), ax.c2p(d["post_m"], float(d["post"].max())), color=POST)
        rows = rows_of([
            (rf"prior: \ centred on {d['prior_m']:g}, \ sd {d['prior_s']:g}", PRIOR),
            (rf"measurement: \ {d['obs']:g}, \ sd {d['like_s']:g}", LIKE),
            (rf"posterior: \ {d['post_m']:.2f}, \ sd {d['post_s']:.2f}", POST),
            (r"between the two, \ nearer the more certain; \ narrower than either", WHITE),
        ], 4.4, 27, 0.34).move_to([4.7, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the normal prior and likelihood multiplied")
        with self.voiceover(
            "With normal distributions everything can be worked out. <bookmark mark='a'/> Here's a prior: the "
            "quantity, which could be a size, a speed or the slant of a surface, is usually near zero, with a "
            "standard deviation of one and a half. <bookmark mark='b'/> Now a measurement comes in, a noisy one. It "
            "says four, with a standard deviation of one. <bookmark mark='c'/> Multiply the two curves, point by "
            "point, and rescale, and you get the posterior. It's centred at two point seven seven, with a standard "
            "deviation of point eight three. <bookmark mark='d'/> Notice two things. The posterior lies between the "
            "prior and the measurement, nearer the more certain of the two. And it's narrower than either: combining "
            "them leaves you more certain than you were with only one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cp), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cq), Create(mark), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def algebra(self):
        d = load("bayes")
        head = heading(r"Why: \ completing the square")
        lines = VGroup(
            MathTex(r"\log p(s \mid x) = -\frac{(x - s)^2}{2\sigma^2} - \frac{(s - \mu_0)^2}{2\sigma_0^2} + \text{const}",
                    font_size=38),
            MathTex(r"= -\frac{1}{2}\Big(\frac{1}{\sigma^2} + \frac{1}{\sigma_0^2}\Big)\, s^2 + "
                    r"\Big(\frac{x}{\sigma^2} + \frac{\mu_0}{\sigma_0^2}\Big)\, s + \text{const}", font_size=38),
            MathTex(r"\frac{1}{\sigma_{\text{post}}^2} = \frac{1}{\sigma^2} + \frac{1}{\sigma_0^2}", font_size=40,
                    color=POST),
            MathTex(r"\mu_{\text{post}} = w\,x + (1 - w)\,\mu_0, \qquad w = \frac{1/\sigma^2}{1/\sigma^2 + 1/\sigma_0^2}",
                    font_size=40, color=POST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.2, 0])
        w = (1 / d["like_s"] ** 2) / (1 / d["like_s"] ** 2 + 1 / d["prior_s"] ** 2)
        rows = rows_of([
            (r"precisions, \ one over the variances, \ add", WHITE),
            (rf"the mean is a weighted average; \ here $w$ = {w:.3f}, \ so $\mu_{{\text{{post}}}}$ = {w:.3f} $\times$ 4 = "
             rf"{d['post_m']:.2f}", WORLD),
        ], 12.0, 28, 0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Here's why, in four lines. <bookmark mark='a'/> Take logs. The log posterior is the log likelihood plus "
            "the log prior: two quadratics in the unknown s, plus a constant. <bookmark mark='b'/> Collect the terms "
            "in s squared and in s. A quadratic in s with a negative leading term is the log of a normal "
            "distribution, so the posterior is normal. <bookmark mark='c'/> Its precision, one over its variance, is "
            "the coefficient of s squared: the precision of the measurement plus the precision of the prior. "
            "Precisions add. <bookmark mark='d'/> And completing the square gives its mean: a weighted average of the "
            "measurement and the prior's mean, with each weighted by its precision. <bookmark mark='e'/> Here the "
            "measurement's weight is point six nine two, and point six nine two times four is two point seven seven. "
            "These two formulas, precisions add and means are precision-weighted, will carry the whole of the next "
            "chapter."
        ) as vo:
            self.play(FadeIn(head))
            for m, ln in zip("abcd", lines):
                vo.wait_until(m)
                self.play(Write(ln), run_time=1.5)
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def shrinkage(self):
        d = load("bayes")
        head = heading(r"Noisier evidence, \ more prior")
        A = axes([0, 4], [0, 4], x_length=6.6, y_length=4.2, xticks=[0, 1, 2, 3, 4], yticks=[0, 1, 2, 3, 4],
                 xlabel=r"the measurement's noise, \ $\sigma$", ylabel=r"the percept, \ $\mu_{\text{post}}$",
                 center=[-2.6, -0.3, 0])
        ax = A.ax
        c = curve(ax, d["lsd"], d["shrink"], POST, stroke_width=5)
        top = DashedLine(ax.c2p(0, d["obs"]), ax.c2p(4, d["obs"]), color=LIKE, stroke_width=2)
        bot = DashedLine(ax.c2p(0, 0.02), ax.c2p(4, 0.02), color=PRIOR, stroke_width=2)
        tl = label(r"what the image says", font_size=22, color=LIKE).next_to(top, UP, buff=0.08).align_to(top, RIGHT)
        rows = rows_of([
            (r"a sharp measurement: \ the percept follows the image", LIKE),
            (r"a noisy one: \ the percept slides toward the prior", PRIOR),
            (r"low contrast, \ dim light, \ a glance: \ all make the measurement noisy", WHITE),
            (r"prediction: \ illusions grow when the evidence gets worse", POST),
        ], 5.0, 27, 0.34).move_to([4.3, -0.1, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the posterior mean as $\sigma$ grows, \ prior N(0, 1.5$^2$)")
        with self.voiceover(
            "Now vary the noise in the measurement, and watch the percept. <bookmark mark='a'/> When the measurement "
            "is sharp, at the left, the percept is almost exactly what the image says, four. <bookmark mark='b'/> As "
            "it gets noisier, the percept slides toward the prior, toward zero. Statisticians call this shrinkage. "
            "<bookmark mark='c'/> And many things make a visual measurement noisy: low contrast, dim light, a brief "
            "glance, the edge of the visual field. <bookmark mark='d'/> So this simple model makes a prediction you "
            "can test: whatever the prior is, its effects, which we'd call illusions, should grow as the evidence "
            "gets worse. In chapter seven we'll see that this is what happens to the speed of things at low contrast."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), Create(top), FadeIn(tl), Create(bot))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def worth(self):
        d = load("bayes")
        head = heading(r"Is a biased percept a bad one?")
        post_var = d["post_s"] ** 2
        b1 = Rectangle(width=6.0, height=0.55, stroke_width=0, fill_color=LIKE, fill_opacity=0.9)
        b2 = Rectangle(width=6.0 * post_var, height=0.55, stroke_width=0, fill_color=POST, fill_opacity=0.9)
        bars = VGroup(
            VGroup(label(r"take the image at its word", font_size=26, color=LIKE), b1).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            VGroup(label(r"the posterior mean", font_size=26, color=POST), b2).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([-2.8, 0.5, 0])
        v1 = label(r"1.00", font_size=26, color=LIKE).next_to(b1, RIGHT, buff=0.2)
        v2 = label(rf"{post_var:.2f}", font_size=26, color=POST).next_to(b2, RIGHT, buff=0.2)
        cap = label(r"mean squared error, \ over worlds drawn from the prior", font_size=24, color=GREY_B)
        cap.next_to(bars, UP, buff=0.4).align_to(bars, LEFT)
        rows = rows_of([
            (r"the posterior mean is biased toward the prior, \ and is right more often", WHITE),
            (rf"its error is the posterior variance, \ {post_var:.2f}, \ against 1 for the raw measurement", POST),
            (r"the price: \ in a world unlike the prior, \ it is confidently wrong", BAD),
            (r"an illusion is often the price of a good bet", PRIOR),
        ], 5.2, 27, 0.34).move_to([4.2, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the normal model's errors")
        with self.voiceover(
            "There's an obvious objection. A percept pulled toward the prior is biased. Isn't that bad? "
            "<bookmark mark='a'/> Compare two strategies, over many worlds drawn from the prior. One takes the image "
            "at its word, and reports the measurement. Its average squared error is the measurement's variance, one. "
            "<bookmark mark='b'/> The other reports the posterior mean. Its average squared error is the posterior's "
            "variance, point six nine: about a third less. Biased, and more accurate. Statisticians call this "
            "the trade between bias and variance; here the brain is the estimator. <bookmark mark='c'/> The "
            "price comes when the world is unlike the prior: a room that isn't rectangular, a picture that only "
            "pretends to have depth. Then the bet is confidently wrong. <bookmark mark='d'/> Which suggests a way of "
            "reading illusions. Many of them aren't failures. They're the price of a bet that pays off almost all the "
            "time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(v1))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(v2), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
