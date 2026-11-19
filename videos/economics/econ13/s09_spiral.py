from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403

PPO = "#7EC8F5"


class Spiral(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The death spiral: \ Harvard, \ 1995--97", r"What happens to a generous insurance plan when its "
             r"price follows its members' costs?", "Chapter seven. The death spiral: Harvard, 1995 to 1997.",
             lit={1998: r"Cutler and Zeckhauser"}, scale=("person", "firm"), horizon=("a year", "a decade"))
        self.harvard()
        self.agora()
        self.lesson()

    def harvard(self):
        sp = load("spiral")
        cz = sp["cz"]
        path_ = sp["harvard"]
        ax = plane([1993.4, 1997.6], [0, 0.25], center=LEFT * 3.0 + DOWN * 0.3, x_length=5.6, y_length=4.6,
                   xticks=[1994, 1995, 1996, 1997], yticks=[0, 0.05, 0.1, 0.15, 0.2], xlabel=r"year",
                   ylabel=r"share of Harvard's employees in the PPO", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%")
        a = ax.ax
        bars = VGroup()
        for yr, charge, share in path_:
            r = Rectangle(width=0.5, height=a.c2p(0, share)[1] - a.c2p(0, 0)[1], stroke_width=0, fill_color=PPO,
                          fill_opacity=0.85).move_to(a.c2p(yr, 0), aligned_edge=DOWN)
            txt = {1994: r"\$400--500", 1995: r"about \$1{,}000", 1996: r"over \$2{,}000"}.get(yr, rf"\${charge:.0f}")
            t = label(txt, font_size=16, color=LEMON).next_to(r, UP, buff=0.1)
            bars.add(VGroup(r, t))
        gone = label(r"disbanded", font_size=18, color=LOSS).move_to(a.c2p(1997, 0.03)).rotate(PI / 2)
        key = label(r"gold: \ the employee's extra charge for the PPO, \ a family, \ 1996 dollars", font_size=14,
                    color=LEMON).next_to(ax, UP, buff=0.05)
        side = VGroup(
            label(rf"about {cz['employees']:,} employees; \\ from {cz['plans_from']}, \ a generous PPO \\ beside "
                  r"several HMOs".replace(",", "{,}"), font_size=20),
            label(r"until 1994 Harvard paid most of the difference: \\ the PPO cost an employee \$400--500 more, \\ "
                  r"and a fifth chose it", font_size=20, color=PPO),
            label(r"1995: \ an equal contribution to every plan \\ (half the staff, \ the rest in 1996); \\ the extra "
                  r"charge doubles, \ to about \$1{,}000", font_size=20, color=LEMON),
            label(r"those who left were younger: \\ average age 46, \ against 51 for those who stayed", font_size=20,
                  color=GREY_A),
            label(r"1996: \ the PPO raises its premium; \\ the charge passes \$2{,}000, \ enrollment 9\%; \\ the leavers "
                  r"were 20\% healthier", font_size=20, color=LOSS),
            label(r"1997: \ the plan is disbanded", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Cutler and Zeckhauser (1998), figures 1.3--1.4; \ Cutler and Reber, QJE 113(2) (1998)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Akerlof's unravelling has been watched happening. <bookmark mark='a'/> Harvard University offered its "
            "ten thousand or so employees a choice of health plans: from 1992, a generous preferred provider "
            "organization, the PPO, run by Blue Cross Blue Shield, beside several cheaper HMOs. "
            "<bookmark mark='b'/> Until 1994 the university paid most of the difference. A family that chose the PPO "
            "paid four to five hundred dollars a year more, and about a fifth of employees chose it. "
            "<bookmark mark='c'/> Then, facing a deficit, Harvard switched to contributing the same amount to every "
            "plan, for half its staff in 1995 and the rest in 1996. The extra charge for the PPO doubled, to about a "
            "thousand dollars, and enrollment fell from twenty percent to fifteen. <bookmark mark='d'/> Those who "
            "left were younger than those who stayed, forty-six years old on average against fifty-one. "
            "<bookmark mark='e'/> Losing its healthier members, the PPO lost money and raised its premium for 1996. "
            "The extra charge passed two thousand dollars, enrollment fell to about nine percent, and Blue Cross found "
            "that those who left that year were twenty percent healthier than average. <bookmark mark='f'/> By the "
            "1997 negotiations, the PPO's price would have had to rise again dramatically. It was disbanded instead. "
            "In David Cutler and Richard Zeckhauser's words, the adverse selection death spiral twisted swiftly."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(key), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(bars[2]), FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(gone), FadeIn(side[5]))
        self.clear_scene()

    def agora(self):
        sp = load("spiral")
        rows = sp["rows"]
        ys = [r["year"] for r in rows]
        ax = plane([-0.6, len(rows) - 0.4], [0, 0.25], center=LEFT * 3.0 + DOWN * 0.3, x_length=5.6, y_length=4.6,
                   xticks=list(range(len(rows))), yticks=[0, 0.05, 0.1, 0.15, 0.2, 0.25], xlabel=r"year",
                   ylabel=r"share enrolled in the generous plan", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%")
        a = ax.ax
        bars = VGroup()
        for r in rows:
            b = Rectangle(width=0.5, height=max(a.c2p(0, r["share"])[1] - a.c2p(0, 0)[1], 1e-3), stroke_width=0,
                          fill_color=PPO, fill_opacity=0.85).move_to(a.c2p(r["year"], 0), aligned_edge=DOWN)
            t = label(rf"\${r['charge']:,.0f}".replace(",", "{,}"), font_size=15, color=LEMON).next_to(b, UP, buff=0.1)
            bars.add(VGroup(b, t))
        r1 = rows[1]
        side = VGroup(
            label(r"Agora's spiral: \ each employee's expected extra cost \\ in the generous plan differs a lot; \ "
                  r"risk aversion \\ makes cover worth 1.5 times that, \ plus a taste", font_size=20),
            label(r"year 0: \ the employer holds the charge at \$450", font_size=20, color=PPO),
            label(r"from then on the plan charges \\ the average extra cost of last year's members", font_size=20,
                  color=LEMON),
            label(rf"those who leave cost \${r1['cost_leavers']:,.0f} on average; \\ those who stay "
                  rf"\${r1['cost_enrolled']:,.0f}".replace(",", "{,}"), font_size=20, color=GREY_A),
            label(r"charge up, \ healthy out, \ cost up, \ charge up", font_size=22, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        tag = agora_tag(corner=DR, font_size=15)
        del ys
        with self.voiceover(
            "Agora can rebuild the mechanism. <bookmark mark='a'/> Each of twenty thousand employees has an expected "
            "extra cost of care in the generous plan, and these differ a great deal. Risk aversion makes the extra "
            "cover worth one and a half times that cost to them, plus a taste for the plan that varies. "
            "<bookmark mark='b'/> In year nought, the employer holds the extra charge at four hundred and fifty "
            "dollars, and about a fifth enroll. <bookmark mark='c'/> From then on, the plan charges the average extra "
            "cost of the people who enrolled the year before. <bookmark mark='d'/> Those who leave are the cheap ones: "
            "in the first year they cost about three hundred dollars on average, those who stay nearly twelve hundred. "
            "<bookmark mark='e'/> So the charge rises, the healthiest leave, the average cost rises, and the charge "
            "rises again. Within four years almost no one is left."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(bars[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[2:]], lag_ratio=0.5), FadeIn(side[4]), run_time=2)
        self.clear_scene()

    def lesson(self):
        cz = load("spiral")["cz"]
        lo, hi = cz["welfare_loss_share"]
        plo, phi = cz["premium_cut"]
        rows = VGroup(
            label(r"was Harvard's reform a mistake?", font_size=27, color=E.ACCENT),
            label(rf"David Cutler and Sarah Reber: \ the selection cost {100 * lo:.0f} to {100 * hi:.0f}\% of what "
                  r"Harvard had been spending", font_size=23, color=LOSS),
            label(rf"but paying the same for every plan made insurers compete: \ premiums fell {100 * plo:.0f} to "
                  rf"{100 * phi:.0f}\%", font_size=23, color=GOOD),
            label(r"and those savings came mostly out of insurers' profits, \ a transfer, \ not a gain", font_size=23,
                  color=GREY_A),
            label(r"the trade-off of every insurance market: \ price competition sorts people by risk", font_size=24,
                  color=SIGNAL),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Cutler and Reber, QJE 113(2) (1998), abstract", corner=DR, font_size=13)
        with self.voiceover(
            "Was the reform a mistake? <bookmark mark='a'/> David Cutler and Sarah Reber estimated that the selection "
            "cost two to four percent of what Harvard had been spending on health insurance. <bookmark mark='b'/> But "
            "paying the same for every plan also made insurers compete for Harvard's employees, and premiums fell by "
            "five to eight percent. <bookmark mark='c'/> Those savings came largely out of the insurers' profits, "
            "which is a transfer to Harvard rather than a gain to society. <bookmark mark='d'/> It is the trade-off "
            "at the heart of every insurance market: price competition is good for prices, but it sorts people by "
            "their risk, and sorting can destroy the cover that the sick most need."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
