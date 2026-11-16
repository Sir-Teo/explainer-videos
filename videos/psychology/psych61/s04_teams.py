from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Teams(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"Big team science", r"What happens when one study is run in dozens of labs?",
                     scale=("society",))
        self.history()
        self.chart()
        self.costs()

    def history(self):
        chips_section(self, r"Many labs, \ one protocol", [
            (r"Many Labs", r"from 2014: \ classic effects run in dozens of labs worldwide with the same protocol", MODEL),
            (r"the Accelerator", r"the Psychological Science Accelerator (2018): \ hundreds of labs in dozens of "
                                 r"countries, \ studies chosen by the network", PERSON),
            (r"ManyBabies", r"infant studies (Part 30) pooled across labs, \ where samples were always tiny", GOOD),
            (r"the costs", r"years per study, \ coordination, \ and credit shared among hundreds of authors", AUTH),
        ], "What happens when one study is run in dozens of labs? <bookmark mark='a'/> From 2014 the Many Labs "
           "projects ran classic effects in dozens of labs worldwide with one protocol. <bookmark mark='b'/> In 2018 "
           "the Psychological Science Accelerator joined hundreds of labs in dozens of countries, with studies "
           "chosen by the network. <bookmark mark='c'/> ManyBabies pooled infant studies, Part 30's subject, across "
           "labs, where samples had always been tiny. <bookmark mark='d'/> The costs: years per study, coordination, "
           "and credit shared among hundreds of authors.", tag=published_tag(r"Moshontz et al.\ (2018)"))

    def chart(self):
        d = load("labs")
        head = heading(r"Forty labs, \ one effect")
        n = len(d["none_est"])
        A = axes([0, n + 1], [-0.3, 1.0], x_length=5.6, y_length=3.2, xticks=None, yticks=[0, 0.3, 0.6, 0.9],
                 yfmt=lambda v: f"{v:g}", ylabel=r"each lab's estimate ($d$)", center=[-3.3, 0.2, 0], font_size=12)
        o1 = np.argsort(d["none_est"])
        o2 = np.argsort(d["het_est"])
        p1 = VGroup(*[Dot(A.ax.c2p(i + 1, float(d["none_est"][j])), radius=0.05, color=MODEL) for i, j in enumerate(o1)])
        p2 = VGroup(*[Dot(A.ax.c2p(i + 1, float(d["het_est"][j])), radius=0.05, color=AUTH) for i, j in enumerate(o2)])
        xl = label(r"labs, \ sorted", font_size=13, color=GREY_A).next_to(A, DOWN, buff=0.1)
        rows = rows_of([
            (r"Psyche's effect, \ $d$ = 0.3, \ run in 40 labs of 100 people each, \ with no true difference "
             r"between labs (purple)", WHITE),
            (rf"the estimates still range from {d['none_est'].min():.2f} to {d['none_est'].max():.2f}: \ sampling "
             rf"error alone, \ your second number", MODEL),
            (rf"with real differences between labs (SD 0.2, \ red), \ $I^2$ rises from {100 * d['none_I2']:.0f}\% "
             rf"to {100 * d['het_I2']:.0f}\%", AUTH),
            (r"Many Labs 2 (Klein and colleagues, \ 2018): \ for most of 28 effects, \ heterogeneity across about 60 "
             r"samples was small; \ a lab's single result mostly reflects sampling, \ not its culture", GOOD),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{community.many\_labs}")
        with self.voiceover(
            "Here's what forty labs look like. <bookmark mark='a'/> Psyche's effect, a d of zero point three, is run in "
            "forty labs of a hundred people each, with no true difference between the labs. <bookmark mark='b'/> The "
            "estimates still range from about minus zero point one to zero point seven. That's sampling error alone, "
            "and your second number. <bookmark mark='c'/> With real differences between labs, the I squared rises "
            "from nineteen percent to thirty-six. <bookmark mark='d'/> In Many Labs 2, Richard Klein and colleagues "
            "found that for most of twenty-eight effects, heterogeneity across about sixty samples was small. A "
            "lab's single result mostly reflects sampling, not its culture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(p) for p in p1], lag_ratio=0.03))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(p) for p in p2], lag_ratio=0.03))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def costs(self):
        chips_section(self, r"What big team science costs", [
            (r"time", r"a protocol agreed by dozens of labs, \ translated, \ approved by each ethics board: \ years, "
                      r"\ not months", AUTH),
            (r"credit", r"hundreds of authors on one paper; \ contribution statements (who designed, \ who ran, \ "
                        r"who analysed) replace the author order", MODEL),
            (r"choice of effect", r"the effects tested are the famous ones; \ a consortium can still pick what is "
                                  r"easy to run online", PERSON),
            (r"what it buys", r"an estimate of the effect and its spread across places, \ which no single lab can "
                              r"give", GOOD),
        ], "What does big team science cost? <bookmark mark='a'/> Time: a protocol agreed by dozens of labs, "
           "translated, and approved by each ethics board takes years, not months. <bookmark mark='b'/> Credit: "
           "hundreds of authors on one paper, so contribution statements, saying who designed, who ran and who "
           "analysed, replace the order of the names. <bookmark mark='c'/> The choice of effect: the effects tested "
           "are the famous ones, and a consortium can still pick what's easy to run online. <bookmark mark='d'/> "
           "And what it buys: an estimate of the effect and its spread across places, which no single lab can give.",
           chip_w=3.8, text_w=8.4)
