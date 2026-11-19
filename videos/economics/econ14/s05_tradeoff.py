from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


class Tradeoff(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Insurance against incentives", r"How large a share should the agent get, \ and what makes it "
             r"smaller?", "Chapter four. Insurance against incentives.",
             lit={1987: r"Holmström and Milgrom", 2002: r"Prendergast's puzzle"}, scale=("person", "firm"),
             horizon=("a year",))
        self.formula()
        self.curves()
        self.evidence()

    def formula(self):
        p = load("playit")
        steps = VGroup(
            label(r"Friday is paid \ $w = \alpha + \beta\,y$, \ where the harvest is \ $y = e + \varepsilon$",
                  font_size=26),
            label(r"Friday picks effort where the share meets the extra cost: \ $\beta = c\,e$, \ so \ $e = \beta / c$",
                  font_size=25, color=EFFORT),
            label(r"the risk Friday carries costs them \ $\tfrac12\, r\, \beta^2 \sigma^2$", font_size=25, color=RISK),
            label(r"what the two of them make together: \ $e - \tfrac12 c\, e^2 - \tfrac12 r\,\beta^2\sigma^2$",
                  font_size=25),
            label(r"$\beta^* \;=\; \dfrac{1}{1 + r\,c\,\sigma^2}$", font_size=46, color=E.ACCENT),
            label(rf"here: \ $r = {p['r']:g}$, \ $c = {p['c']:g}$, \ $\sigma = {p['sigma']:g}$, \ so \ "
                  rf"$\beta^* = 1/(1 + {p['r'] * p['c'] * p['sigma'] ** 2:g}) = 2/3$", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.05)
        tag = published_tag(r"Holmström and Milgrom, Econometrica 55(2) (1987)", corner=DR, font_size=13)
        with self.voiceover(
            "Friday's contract in the Play it had a formula behind it, from Bengt Holmström and Paul Milgrom in 1987. "
            "<bookmark mark='a'/> Friday is paid a fixed amount plus a share beta of the harvest, which is effort plus "
            "luck. <bookmark mark='b'/> Friday works until the share of one more basket matches the cost of the "
            "effort it takes, so effort is the share divided by c, a number for how quickly effort grows tiring. "
            "<bookmark mark='c'/> The luck Friday carries costs them one half times r, their dislike of risk, times "
            "the share squared, times the variance of the luck. <bookmark mark='d'/> The fixed pay only moves money "
            "between them, so the best share is the one that makes the most for the two together: the harvest, less "
            "the cost of the effort, less the cost of the risk. <bookmark mark='e'/> And that share is one over one "
            "plus r times c times sigma squared. <bookmark mark='f'/> In the Play it, r times c times sigma squared "
            "was a half, so the best share was two-thirds."
        ) as vo:
            self.play(FadeIn(steps[0]), FadeIn(tag))
            for mk, r in zip("bcdef", steps[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def curves(self):
        t = load("tradeoff")
        sig = np.array(t["sigma"])
        cols = [EFFORT, PAY, RISK]
        names = [r"", r"Friday: \ ", r""]
        ax = plane([0, 10], [0, 1.05], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.4, y_length=4.6,
                   xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.25, 0.5, 0.75, 1], xlabel=r"luck in the harvest, \ "
                   r"$\sigma$ \ (baskets)", ylabel=r"the best share, \ $\beta^*$", font_size=16,
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}")
        a = ax.ax
        cs = VGroup(*[path(ax, sig, cur, color=col, width=3) for cur, col in zip(t["curves"], cols)])
        ls = VGroup(*[label(rf"{nm}$r = {r:g}$", font_size=15, color=col).next_to(a.c2p(10, cur[-1]), RIGHT, buff=0.1)
                      for nm, r, cur, col in zip(names, t["rs"], t["curves"], cols)])
        here = t["here"]
        hd = Dot(a.c2p(5, here["beta_star"]), radius=0.09, color=E.ACCENT)
        hl = label(r"the Play it", font_size=15, color=E.ACCENT).next_to(hd, UR, buff=0.06)
        side = VGroup(
            label(r"no luck: \ give Friday everything, \\ the grove is as good as theirs", font_size=21),
            label(r"more luck, \ or more dislike of it \\ (green: barely minds risk; \ red: minds it a lot): "
                  r"\\ a smaller share, \ more insurance", font_size=21, color=GREY_A),
            label(r"and effort that responds strongly \\ (a small $c$) \ calls for a larger share", font_size=21,
                  color=PAY),
            label(rf"what not seeing effort costs here: \\ {here['agency_cost']:.2f} of the "
                  rf"{here['first_best_surplus']:.0f} baskets a day", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Draw the best share against the luck in the harvest. <bookmark mark='a'/> With no luck at all, the "
            "harvest shows effort exactly, so give Friday everything: Friday pays a fixed rent, and the grove is as "
            "good as theirs. <bookmark mark='b'/> The more luck there is, and the more Friday dislikes it, the "
            "smaller the share, and the more of the luck Crusoe takes on as insurance. Three Fridays: one who barely "
            "minds risk, ours, and one who minds it a great deal. <bookmark mark='c'/> And where effort responds "
            "strongly to pay, a larger share is worth its risk. <bookmark mark='d'/> At the Play it's numbers, not "
            "seeing effort costs a third of everything the two of them could have made."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(cs[1]), FadeIn(ls[1]))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(ax.ax.y_axis, color=EFFORT))
            vo.wait_until("b")
            self.play(Create(cs[0]), Create(cs[2]), FadeIn(ls[0]), FadeIn(ls[2]), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(hd, scale=1.5), FadeIn(hl), FadeIn(side[3]))
        self.clear_scene()

    def evidence(self):
        rows = VGroup(
            label(r"the prediction: \ riskier jobs, \ weaker incentives", font_size=26, color=E.ACCENT),
            label(r"the evidence, \ surveyed by Canice Prendergast: \ mixed, \ and often the opposite", font_size=24,
                  color=RISK),
            label(r"franchised outlets in riskier places, \ executives of volatile firms: \ often more pay "
                  r"for results, \ not less", font_size=22, color=GREY_A),
            label(r"Prendergast's explanation: \ where things are uncertain, \ the principal can't tell the agent what to do",
                  font_size=23, color=SIGNAL),
            label(r"so it delegates, \ and pays on results \ because watching inputs tells little there", font_size=23,
                  color=SIGNAL),
            label(r"the trade-off is real, \ but uncertainty also changes what can be watched", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.33).move_to(UP * 0.1)
        tag = published_tag(r"Prendergast, JEL 37(1) (1999); \ JPE 110(5) (2002)", corner=DR, font_size=13)
        with self.voiceover(
            "This is a clean prediction, and economists went looking for it. <bookmark mark='a'/> Riskier jobs should "
            "have weaker incentives. <bookmark mark='b'/> Canice Prendergast surveyed the studies in 1999. The "
            "evidence is mixed, and it often goes the other way. <bookmark mark='c'/> Outlets in riskier places are "
            "more often franchised, which hands the manager the profit, and executives of volatile firms are often "
            "paid more, not less, on results. <bookmark mark='d'/> In 2002 Prendergast offered an explanation: where "
            "things are uncertain, the principal doesn't know what the agent ought to be doing. "
            "<bookmark mark='e'/> So the principal delegates, and pays on results, because watching the agent's "
            "inputs tells you little there. <bookmark mark='f'/> The trade-off between insurance and incentives is "
            "real, but uncertainty also changes what the principal can watch, and that can outweigh it."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
