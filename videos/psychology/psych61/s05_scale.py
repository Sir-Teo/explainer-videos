from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Scale(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"Millions of participants", r"What can a sample of a million fix?", scale=("society",))
        self.examples()
        self.selection()
        self.meng()

    def examples(self):
        chips_section(self, r"Experiments at the scale of millions", [
            (r"navigation", r"Sea Hero Quest: \ a phone game whose levels measure spatial navigation, \ played by "
                            r"millions in dozens of countries (Coutrot and colleagues, \ 2018)", MODEL),
            (r"moral choices", r"the Moral Machine: \ about 40 million decisions about whom a driverless car "
                               r"should spare, \ from 233 countries and territories (Awad and colleagues, \ 2018)",
             PERSON),
            (r"language learning", r"a grammar quiz taken by about 670,000 people, \ used to estimate when the "
                                   r"ability to learn a language declines (Hartshorne and colleagues, \ 2018)", GOOD),
        ], "What can a sample of a million fix? Here are experiments at that scale. <bookmark mark='a'/> Sea Hero "
           "Quest, a phone game whose levels measure spatial navigation, was played by millions of people in dozens "
           "of countries, as Antoine Coutrot and colleagues reported in 2018. <bookmark mark='b'/> The Moral Machine "
           "collected about forty million decisions about whom a driverless car should spare, from two hundred and "
           "thirty-three countries and territories. <bookmark mark='c'/> And a grammar quiz taken by about six "
           "hundred and seventy thousand people was used to estimate when the ability to learn a language declines.",
           tag=published_tag(r"Awad et al.\ (2018)"), chip_w=3.2, text_w=9.0)

    def selection(self):
        d = load("selection")
        head = heading(r"Noise shrinks; \ bias does not")
        x = np.log10(np.asarray(d["n"]))
        A = axes([1.6, 6.4], [-0.1, 0.6], x_length=5.6, y_length=3.2, xticks=[2, 3, 4, 5, 6], yticks=[0, 0.2, 0.4],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: f"{v:g}", xlabel=r"people in the sample",
                 ylabel=r"estimated mean", center=[-3.3, 0.2, 0], font_size=12)
        truth = DashedLine(A.ax.c2p(1.6, 0), A.ax.c2p(6.4, 0), color=GOOD, stroke_width=2)
        bars_ = VGroup(*[VGroup(Line(A.ax.c2p(xx, m - h), A.ax.c2p(xx, m + h), color=AUTH, stroke_width=4),
                                Dot(A.ax.c2p(xx, m), radius=0.06, color=AUTH))
                         for xx, m, h in zip(x, d["mean"], d["half"])])
        rows = rows_of([
            (r"Psyche's population has a true mean of 0; \ people who score higher are a little more likely to "
             r"volunteer", WHITE),
            (r"from a hundred to a million volunteers, \ the 95\% interval shrinks a hundredfold", MODEL),
            (rf"it shrinks around {d['mean'][-1]:.2f}, \ not 0: \ your third number", AUTH),
            (r"size fixes noise; \ it does not fix who chose to take part, \ or what a game measures (Part 3's "
             r"validity)", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{community.selected\_sample}")
        with self.voiceover(
            "But size fixes only one thing. <bookmark mark='a'/> Psyche's population has a true mean of zero, and "
            "people who score higher are a little more likely to volunteer. <bookmark mark='b'/> From a hundred to a "
            "million volunteers, the ninety-five percent interval shrinks a hundredfold. <bookmark mark='c'/> It "
            "shrinks around zero point two two, not zero. That's your third number. <bookmark mark='d'/> Size fixes "
            "noise. It doesn't fix who chose to take part, or what a game measures, which is Part 3's validity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(truth))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(b) for b in bars_], lag_ratio=0.3))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def meng(self):
        rho, N, f = 0.005, 300e6, 0.01
        n_eff = f / ((1 - f) * rho ** 2)
        rows_section(self, r"How big is a biased million?", [
            (r"Meng, \ 2018: \ the error of a sample mean is the product of three things: \ the correlation between "
             r"taking part and the answer ($\rho$), \ the share of the population not sampled, \ and the spread of "
             r"the answer", WHITE),
            (r"$\bar y_n - \bar y_N = \rho \times \sqrt{(N - n)/n} \times \sigma$: \ with no randomization, \ $\rho$ "
             r"does not shrink as $n$ grows", MODEL),
            (rf"worked: \ $\rho$ = 0.005, \ a tiny tilt; \ a population of 300 million; \ a 1\% sample of 3 million",
             PERSON),
            (rf"its error is that of a simple random sample of about {n_eff:.0f} people", AUTH),
            (r"a small random sample can beat a huge self-selected one: \ for estimating a mean, \ how people were "
             r"chosen matters more than how many", YOU),
        ], "How big is a biased million? <bookmark mark='a'/> In 2018 Xiao-Li Meng wrote the error of a sample mean "
           "as a product of three things: the correlation between taking part and the answer, the share of the "
           "population not sampled, and the spread of the answer. <bookmark mark='b'/> Without randomization, that "
           "correlation doesn't shrink as the sample grows. <bookmark mark='c'/> Worked through: a correlation of "
           "zero point zero zero five, a tiny tilt, in a population of three hundred million, with a one percent "
           "sample of three million people. <bookmark mark='d'/> Its error is that of a simple random sample of "
           "about four hundred. <bookmark mark='e'/> A small random sample can beat a huge self-selected one. For "
           "estimating a mean, how people were chosen matters more than how many.",
           font_size=21)
