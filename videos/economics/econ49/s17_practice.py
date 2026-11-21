from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ crime, \ schools and health", r"Who uses these ideas, and how?",
             "Chapter fifteen. In practice: crime, schools and health.", lit={1995: r"DiIulio"},
             scale=("city", "nation"), horizon=("a year", "a decade"))
        self.people()
        self.called()

    def people(self):
        rows = VGroup(
            label(r"police chiefs and city budgets: \ how many officers, \ and where to put them", font_size=21,
                  color=POLICE),
            label(r"sentencing commissions and parole boards: \ certainty against severity, \ the cost of prison",
                  font_size=21, color=FINE),
            label(r"school districts: \ class sizes, \ teacher hiring and pay, \ lotteries for places", font_size=21,
                  color=SCHOOL),
            label(r"health systems and insurers: \ co-payments, \ hospital mergers, \ drug prices and patents",
                  font_size=21, color=HEALTH),
            label(r"welfare offices and statisticians: \ who receives a benefit, \ and what families need",
                  font_size=21, color=WOMEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.2)
        head = label(r"the people who use this", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Who uses the economic approach to everyday life? <bookmark mark='a'/> Police chiefs and city "
            "budgets, deciding how many officers to hire and where to send them, with estimates like those of "
            "chapter three. <bookmark mark='b'/> Sentencing commissions and parole boards, weighing the certainty "
            "of punishment against its length, and the cost of a year in prison. <bookmark mark='c'/> School "
            "districts, choosing class sizes, hiring and paying teachers, and running lotteries for places that "
            "double as experiments. <bookmark mark='d'/> Health systems and insurers, setting co-payments, "
            "reviewing hospital mergers and negotiating drug prices. <bookmark mark='e'/> And welfare offices and "
            "statisticians, deciding whom a benefit should be paid to, the lesson of chapter seven."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["diiulio_1995"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=18)
        cc.move_to(UP * 1.5)
        ax = plane([1989, 2011], [0, 160], center=DOWN * 2.0 + LEFT * 0.8, x_length=7.6, y_length=2.6,
                   xticks=[1990, 1995, 2000, 2005, 2010], yticks=[0, 50, 100, 150], xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda x: f"{x:.0f}", font_size=12)
        yl = label(r"juvenile arrests for violent crime, \ rate, \ 1994 = 100", font_size=13,
                   color=GREY_A).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        pred = DashedLine(ax.ax.c2p(1995, 100), ax.ax.c2p(2010, 150), color=LOSS, stroke_width=2.4)
        pred_l = label(r"the forecast: \ up \ (schematic)", font_size=13, color=LOSS).next_to(
            ax.ax.c2p(2010, 150), LEFT, buff=0.1)
        p94 = dot(ax, 1994, 100, WHITE, 0.07)
        p04 = dot(ax, 2004, 50, GAIN, 0.07)
        act = DashedLine(ax.ax.c2p(1994, 100), ax.ax.c2p(2004, 50), color=GAIN, stroke_width=2.4)
        act_l = label(r"2004: \ half", font_size=13, color=GAIN).next_to(p04, DOWN, buff=0.1)
        cap = label(r"two points from OJJDP's \\ bulletins; \ the path \\ between them is not \\ drawn from data",
                    font_size=12, color=GREY_A).next_to(ax, RIGHT, buff=0.35)
        tag = published_tag(r"DiIulio, \ The Weekly Standard (1995); \ OJJDP bulletins", corner=DL, font_size=11)
        with self.voiceover(
            "Called it? A forecast about crime. <bookmark mark='a'/> In November 1995 the political scientist John "
            "DiIulio warned of a coming wave of juvenile super-predators: some two hundred and seventy thousand more "
            "young predators on American streets by 2010 than in 1990. The projection rested on the number of boys "
            "who would be teenagers and on the rise in youth violence of the early 1990s. <bookmark mark='b'/> "
            "What happened: juvenile violence had already turned. <bookmark mark='c'/> By 2004 the arrest rate of "
            "juveniles for violent crime was half its 1994 peak. <bookmark mark='d'/> The verdict: wrong. DiIulio "
            "later said so himself, but by then most states had passed laws making it easier to try children as "
            "adults. A forecast that extrapolates a trend, without a model of why people offend, is a forecast of "
            "the past."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(yl), FadeIn(p94), run_time=1.0)
            self.play(Create(pred), FadeIn(pred_l), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(Create(act), FadeIn(p04), FadeIn(act_l), FadeIn(cap), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
