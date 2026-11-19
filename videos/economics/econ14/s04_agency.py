from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


class Agency(VoiceoverScene):
    def construct(self):
        card(self, 3, r"The principal--agent problem", r"Two efforts, \ two harvests: \ what is the cheapest pay that "
             r"buys hard work?", "Chapter three. The principal-agent problem.",
             lit={1973: r"Ross", 1975: r"Mirrlees", 1979: r"Holmström", 1983: r"Grossman and Hart"},
             scale=("person", "firm"), horizon=("a season",))
        self.setting()
        self.solve()
        self.wages()
        self.lessons()

    def setting(self):
        d = load("discrete")
        ph, pl = d["p_high"], d["p_low"]
        ax = plane([0, 3], [0, 1.05], center=LEFT * 3.2 + DOWN * 0.4, x_length=5.4, y_length=4.4, xticks=[],
                   yticks=[0, 0.5, 1], xlabel="", ylabel=r"chance", font_size=16, yfmt=lambda v: f"{v:.1f}")
        a = ax.ax
        bars = VGroup()
        for x0, p, col, name in ((0.55, ph, EFFORT, r"works hard"), (1.95, pl, GREY_B, r"takes it easy")):
            good = Rectangle(width=0.5 * a.x_axis.get_unit_size(), height=p * a.y_axis.get_unit_size(),
                             stroke_width=0, fill_color=col, fill_opacity=0.85)
            good.move_to(a.c2p(x0, 0), aligned_edge=DOWN)
            bad = Rectangle(width=0.5 * a.x_axis.get_unit_size(), height=(1 - p) * a.y_axis.get_unit_size(),
                            stroke_width=0, fill_color=RISK, fill_opacity=0.55)
            bad.move_to(a.c2p(x0 + 0.5, 0), aligned_edge=DOWN)
            t1 = label(rf"good: \\ {p:.0%}".replace("%", r"\%"), font_size=16, color=col).next_to(good, UP, buff=0.08)
            t2 = label(rf"poor: \\ {1 - p:.0%}".replace("%", r"\%"), font_size=16, color=RISK).next_to(bad, UP,
                                                                                                    buff=0.08)
            nm = label(name, font_size=17, color=col).next_to(a.c2p(x0 + 0.25, 0), DOWN, buff=0.2)
            bars.add(VGroup(good, bad, t1, t2, nm))
        key = label(r"a good harvest: \ 100 baskets; \ a poor one: \ 40", font_size=16, color=GREY_A).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        side = VGroup(
            VGroup(pair(height=0.6), label(r"the principal, \ Crusoe, \ sees only the harvest; \\ the agent, \ "
                                          r"Friday, \ chooses the effort", font_size=20)).arrange(RIGHT, buff=0.3),
            label(r"hard work makes a good harvest likelier, \\ but doesn't guarantee one", font_size=21,
                  color=EFFORT),
            label(r"Friday values pay by its logarithm: \\ each doubling of pay is worth the same", font_size=21,
                  color=PAY),
            label(r"working hard costs Friday 0.3 of that scale; \\ other work is worth 2.0", font_size=21, color=RISK),
            label(r"the principal pays $w_H$ after a good harvest, \\ $w_L$ after a poor one", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The economists' name for this is the principal-agent problem: the principal, here Crusoe, wants the "
            "agent, Friday, to act, and sees only a noisy result. Stephen Ross posed it in these terms in 1973; James Mirrlees and "
            "Bengt Holmström worked out its logic in the 1970s. Take the simplest version. <bookmark mark='a'/> "
            "Friday either works hard or takes it easy. <bookmark mark='b'/> Hard work makes a good harvest of a "
            "hundred baskets likely, eighty percent; taking it easy makes it less likely than not, forty percent. "
            "Otherwise the harvest is a poor forty baskets. <bookmark mark='c'/> Friday values pay by its logarithm, "
            "so each doubling of pay is worth the same to them; that is what disliking risk looks like here. "
            "<bookmark mark='d'/> Hard work costs Friday three tenths on that scale, and other work is worth two. "
            "<bookmark mark='e'/> Crusoe pays one wage after a good harvest and another after a poor one."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][4]), FadeIn(bars[1][4]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b[k], DOWN) for b in bars for k in (0, 1)], FadeIn(key), FadeIn(side[1]))
            self.play(*[FadeIn(b[k]) for b in bars for k in (2, 3)])
            for mk, r in zip("cde", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def solve(self):
        d = load("discrete")
        ph, pl, cost, res = d["p_high"], d["p_low"], d["cost"], d["reservation"]
        uL, uH = np.log(d["w_low"]), np.log(d["w_high"])
        ufb = res + cost
        ax = plane([0.8, 3.2], [0.8, 3.2], center=LEFT * 3.0 + DOWN * 0.25, x_length=5.2, y_length=5.2,
                   xticks=[1, 1.5, 2, 2.5, 3], yticks=[1, 1.5, 2, 2.5, 3], xlabel=r"Friday's utility after a poor "
                   r"harvest, \ $\ln w_L$", ylabel=r"after a good one, \ $\ln w_H$", font_size=15,
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}")
        a = ax.ax
        diag = seg(ax, 0.8, 0.8, 3.2, 3.2, color=GREY_B, width=1.5, dashed=True)
        dl = label(r"dashed: \ full insurance, \\ the same pay either way", font_size=14, color=GREY_B).move_to(
            a.c2p(2.75, 1.1))
        # participation: ph uH + (1 - ph) uL = ufb
        pc = lambda x: (ufb - (1 - ph) * x) / ph
        part = seg(ax, 1.0, pc(1.0), 3.2, pc(3.2), color=PAY, width=3)
        partl = label(r"takes the job, \ above", font_size=14, color=PAY).next_to(a.c2p(3.15, pc(3.15)), DOWN,
                                                                                  buff=0.12, aligned_edge=RIGHT)
        # incentive compatibility: uH - uL = cost / (ph - pl)
        gap = cost / (ph - pl)
        ic = seg(ax, 0.8, 0.8 + gap, 3.2 - gap, 3.2, color=EFFORT, width=3)
        icl = label(r"works hard, \ above", font_size=14, color=EFFORT).rotate(PI / 4).move_to(
            a.c2p(2.2, 2.2 + gap) + np.array([-0.22, 0.22, 0]))
        # the region above both lines
        top = 3.2
        xs = np.linspace(0.8, 3.2 - gap, 60)
        lower = [max(pc(x), x + gap) for x in xs]
        poly = Polygon(*[a.c2p(x, y) for x, y in zip(xs, lower)], a.c2p(0.8, top), stroke_width=0,
                       fill_color=E.ACCENT, fill_opacity=0.12)
        fb = Dot(a.c2p(ufb, ufb), radius=0.08, color=GREY_A)
        fbl = label(r"if effort could be seen", font_size=14, color=GREY_A).move_to(a.c2p(2.75, 1.55))
        fba = Arrow(fbl.get_top(), fb.get_center(), buff=0.1, color=GREY_A, stroke_width=2, tip_length=0.12)
        sb = Dot(a.c2p(uL, uH), radius=0.1, color=E.ACCENT)
        sbl = label(r"the cheapest pay \\ that buys hard work", font_size=15, color=E.ACCENT).move_to(a.c2p(1.2, 3.0))
        sba = Arrow(sbl.get_bottom(), sb.get_center(), buff=0.1, color=E.ACCENT, stroke_width=2, tip_length=0.12)
        side = VGroup(
            label(r"take the job: \\ $0.8\,\ln w_H + 0.2\,\ln w_L - 0.3 \ \ge\ 2$", font_size=21, color=PAY),
            label(r"work hard rather than not: \\ $(0.8 - 0.4)(\ln w_H - \ln w_L)\ \ge\ 0.3$", font_size=21,
                  color=EFFORT),
            label(r"so $\ln w_H$ must beat $\ln w_L$ by at least $0.75$", font_size=21, color=EFFORT),
            label(r"the cheapest contract sits where both bind", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Holmström, Bell Journal 10(1) (1979); \ Grossman and Hart, Econometrica 51(1) (1983)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Crusoe wants hard work, and wants it as cheaply as possible. Two conditions must hold. Draw each contract "
            "as a point: what Friday's pay is worth to them after a poor harvest, across, and after a good one, up. "
            "<bookmark mark='a'/> First, Friday must take the job: the pay, averaged over the harvests that hard work "
            "brings, less the effort, must be worth at least the other work. That is everything above this line. "
            "<bookmark mark='b'/> Second, Friday must prefer working hard to taking it easy. Working hard raises the "
            "chance of the good harvest by forty points, so the gap between the two pays, times forty percent, must "
            "cover the effort. <bookmark mark='c'/> The good-harvest pay must beat the poor-harvest pay by three "
            "quarters on Friday's scale: everything above this second line. <bookmark mark='d'/> The contracts that "
            "work are above both lines, and the cheapest is the corner where both just hold. If Crusoe could see "
            "effort, he would pay the same whatever the harvest, on the dashed line of full insurance. He can't, so "
            "the contract must leave Friday exposed."
        ) as vo:
            self.play(FadeIn(ax), Create(diag), FadeIn(dl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(part), FadeIn(partl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ic), FadeIn(icl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(poly))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(sb, scale=1.5), FadeIn(sbl), GrowArrow(sba))
            self.play(FadeIn(fb), FadeIn(fbl), GrowArrow(fba))
        self.clear_scene()

    def wages(self):
        d = load("discrete")
        heads = [r"", r"after a good \\ harvest", r"after a poor \\ harvest", r"Crusoe's \\ expected cost",
                 r"Crusoe's \\ expected profit"]
        xs = [-4.6, -1.6, 0.6, 2.9, 5.2]
        head = VGroup(*[label(h, font_size=19, color=GREY_B).move_to(RIGHT * x + UP * 2.3) for h, x in zip(heads, xs)])
        rule = Line(LEFT * 6.2 + UP * 1.75, RIGHT * 6.4 + UP * 1.75, color=GREY_C, stroke_width=1.5)

        def row(name, wh, wl, cost, prof, y, col):
            return VGroup(
                label(name, font_size=21, color=col).move_to(RIGHT * xs[0] + UP * y),
                label(f"{wh:.2f}", font_size=23, color=PAY).move_to(RIGHT * xs[1] + UP * y),
                label(f"{wl:.2f}", font_size=23, color=PAY).move_to(RIGHT * xs[2] + UP * y),
                label(f"{cost:.2f}", font_size=23, color=RISK).move_to(RIGHT * xs[3] + UP * y),
                label(f"{prof:.2f}", font_size=24, color=col).move_to(RIGHT * xs[4] + UP * y))

        r1 = row(r"if effort could be seen: \\ hard work, \ a flat wage", d["fb_wage"], d["fb_wage"], d["fb_wage"],
                 d["profit_fb"], 1.15, GREY_A)
        r2 = row(r"it can't: \\ hard work, \ the cheapest pair", d["w_high"], d["w_low"], d["cost_hard"],
                 d["profit_hard"], 0.05, E.ACCENT)
        r3 = row(r"or settle for easy work, \\ a flat wage", d["flat_easy"], d["flat_easy"], d["flat_easy"],
                 d["profit_easy"], -1.05, GREY_B)
        foot = VGroup(
            label(rf"the premium for risk: \ {d['cost_hard']:.2f} $-$ {d['fb_wage']:.2f} $=$ {d['risk_cost']:.2f} "
                  r"baskets a season", font_size=22, color=RISK),
            label(r"worth paying: \ hard work still earns Crusoe far more than easy work", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Turn the corner back into baskets. <bookmark mark='a'/> If Crusoe could see effort, a flat wage of about "
            "ten baskets would buy hard work. <bookmark mark='b'/> He can't, so the cheapest pair is eleven point six "
            "after a good harvest and five point five after a poor one. On average that costs him ten point four, "
            "<bookmark mark='c'/> or about four tenths of a basket more: a premium to compensate Friday for bearing "
            "risk that a contract on effort would have spared them. <bookmark mark='d'/> It is still worth paying. "
            "With a flat wage, Friday would take it easy, and Crusoe's profit would fall from about seventy-eight "
            "baskets to fifty-seven."
        ) as vo:
            self.play(FadeIn(head), Create(rule), FadeIn(r1))
            vo.wait_until("b")
            self.play(FadeIn(r2))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(r3), FadeIn(foot[1]))
        self.clear_scene()

    def lessons(self):
        rows = VGroup(
            label(r"Crusoe knows Friday works hard: \ the contract makes sure of it", font_size=24),
            label(r"yet he still pays less after a poor harvest", font_size=24, color=RISK),
            label(r"the pay is not a reward for the harvest: \ it is an inference about effort", font_size=24,
                  color=SIGNAL),
            label(r"pay rises with outcomes that are likelier under hard work \ (the likelihood ratio)", font_size=24,
                  color=EFFORT),
            label(r"so the best contract need not rise with output: \ it rises with what output reveals", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Mirrlees, RES 66(1) (1999; written 1975); \ Holmström, Bell Journal 10(1) (1979)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "There is something strange here. <bookmark mark='a'/> Crusoe knows Friday works hard, because the "
            "contract makes sure of it. <bookmark mark='b'/> Yet he still pays less after a poor harvest, knowing it "
            "was bad luck. <bookmark mark='c'/> The pay is not a reward for the harvest, and not a punishment either. "
            "It is there so that, had Friday shirked, the harvest would have shown it. <bookmark mark='d'/> Mirrlees "
            "and Holmström showed that in the best contract, pay rises with outcomes that are likelier under hard "
            "work than under shirking: statisticians call that comparison the likelihood ratio. "
            "<bookmark mark='e'/> So the best contract need not rise with output at all. It rises with what output "
            "reveals about effort."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
