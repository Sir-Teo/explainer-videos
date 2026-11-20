from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Health(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Health insurance and moral hazard", r"How much does insurance raise spending, and is it "
                                                            r"worth it?",
             "Chapter six. Health insurance and moral hazard.", lit={1963: r"Arrow", 1968: r"Pauly",
                                                                     1987: r"Manning et al."},
             scale=("person", "household"), horizon=("a year",))
        self.rand()
        self.tradeoff()
        self.lessons()

    def rand(self):
        R = tables.RAND_HIE.data
        plans = [(r"free care", 100, HEALTH), (r"25\% coinsurance", 100 - R["less_25"], HEALTH),
                 (r"95\% coinsurance", 100 - R["less_95"], HEALTH)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(plans):
            x = -3.2 + 2.4 * k
            h = v * 0.035
            r = Rectangle(width=1.4, height=h, stroke_width=0, fill_color=col, fill_opacity=0.35 + 0.006 * v).move_to(
                np.array([x, -2.4 + h / 2, 0]))
            bars.add(VGroup(r, label(nm, font_size=18, color=WHITE).next_to(r, DOWN, buff=0.15),
                            label(f"{v}", font_size=24, color=col).next_to(r, UP, buff=0.12)))
        side = VGroup(
            label(rf"{R['families']:,} families, \\ more than {R['people']:,} people, \\ {R['sites']} sites, "
                  r"\\ the 1970s to 1982", font_size=18, color=GREY_A),
            label(r"assigned at random to \\ free care or to paying \\ 25\%, \ 50\% or 95\% \\ of the bill \ "
                  r"(capped)", font_size=18, color=WHITE),
            label(r"spending, \ free care = 100", font_size=18, color=HEALTH),
            label(r"health, \ on average: \\ not measurably worse", font_size=19, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = published_tag(tables.RAND_HIE.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Kenneth Arrow argued in 1963 that medical care is unlike other goods: illness is uncertain, and doctors "
            "know far more than their patients. Insurance protects against the cost of illness, but it also lowers "
            "the price of care at the moment of use, so people use more of it, which Mark Pauly called moral "
            "hazard. How much more? <bookmark mark='a'/> From the 1970s to 1982 the RAND Corporation ran the largest "
            "social experiment of its time: 2,750 families, more than 7,700 people, at six sites. "
            "<bookmark mark='b'/> Each family was assigned at random to free care, or to paying a quarter, a half "
            "or ninety-five percent of its medical bills, with a cap related to income. <bookmark mark='c'/> Those "
            "paying ninety-five percent spent about thirty percent less than those with free care; those paying a "
            "quarter, about twenty percent less. <bookmark mark='d'/> And on average their health was not "
            "measurably worse, though some of the poorest and sickest did worse with less care."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(side[0]), FadeIn(bars[0][0]), FadeIn(bars[0][1]), run_time=1.2)
            vo.wait_until("a")
            self.play(Indicate(side[0], color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(bars[0][2]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), *[GrowFromEdge(b_[0], DOWN) for b_ in bars[1:]],
                      *[FadeIn(b_[1:]) for b_ in bars[1:]])
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def tradeoff(self):
        H = load("health")
        c = np.array(H["c"])
        rp = 100 * np.array(H["risk_premium"])
        ov = 100 * np.array(H["overuse"])
        tot = rp + ov
        ax = plane([0, 1], [0, 4.5], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 1, 2, 3, 4],
                   xlabel=r"coinsurance: \ the share of each bill the patient pays",
                   ylabel=r"cost, \ percent of income", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        l_rp = path(ax, c, rp, RISK, 3.2)
        l_ov = path(ax, c, ov, HAZARD, 3.2)
        l_t = path(ax, c, tot, WHITE, 3.6)
        at = H["at"]
        star = VGroup(vline(ax, H["cstar"], 0, 4.5, GAIN),
                      dot(ax, H["cstar"], 100 * (at["risk_premium"] + at["overuse"]), GAIN, 0.09))
        side = VGroup(
            label(r"purple: \ the risk \\ the patient still bears", font_size=18, color=RISK),
            label(r"gold: \ care worth less \\ than it costs, \ bought \\ because it is cheap", font_size=18,
                  color=HAZARD),
            label(r"white: \ the sum", font_size=18, color=WHITE),
            label(rf"the best plan: \\ the patient pays {100 * H['cstar']:.0f}\%", font_size=20, color=GAIN),
            label(rf"the Island's patients: \\ the 95\% plan spends \\ {100 * H['less95']:.0f}\% less than free care",
                  font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "So insurance has a cost as well as a benefit, and the best plan trades them off, a problem Richard "
            "Zeckhauser set out in 1970. On the Island, illnesses of every size strike seven in ten people a year, "
            "and care repairs the harm with diminishing returns. <bookmark mark='a'/> The less of each bill a "
            "patient pays, the less risk they bear: the purple line falls to zero with free care. "
            "<bookmark mark='b'/> But the less they pay, the more care they buy that is worth less than it costs: "
            "the gold line rises as coinsurance falls. <bookmark mark='c'/> The white line is the sum. "
            f"<bookmark mark='d'/> It is lowest when patients pay about {say_pct(H['cstar'], 0)} of each bill. "
            "<bookmark mark='e'/> The Island is set so that, as in RAND, patients paying ninety-five percent spend "
            "thirty percent less than with free care. Real plans also cap what anyone pays in a year, which removes "
            "most of the remaining risk while keeping a price on the first visits."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            self.play(Create(l_rp), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(l_rp, color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(Create(l_ov), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(l_t), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(star), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def lessons(self):
        H = load("health")
        cards = point_cards([
            (r"the elasticity", rf"RAND's summary: \\ about $-$0.2; \\ the Island: \ $-${abs(H['arc']):.2f}",
             HEALTH),
            (r"a fragile number", r"deductibles and caps \\ mean no single price \\ applies \ (Aron-Dine, \\ Einav "
                                  r"and Finkelstein)", HOLD),
            (r"what was cut", r"care that helped \\ and care that did not, \\ alike", LOSS),
            (r"the design", r"cheap care that \\ prevents, \ dear \\ care of low value", GAIN),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what moral hazard in health care means", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.RAND_HIE.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Four lessons. <bookmark mark='a'/> RAND's response is often summarized as a price elasticity of about "
            f"minus 0.2. On the Island, between the twenty-five and ninety-five percent plans, it is "
            f"{say_num(H['arc'], 2)}. <bookmark mark='b'/> But Aliza Aron-Dine, Liran Einav and Amy Finkelstein "
            "showed that the summary is fragile: with deductibles and caps there is no single price, and the "
            "number depends on which one is used. <bookmark mark='c'/> Patients who paid more cut care that was "
            "highly effective "
            "in roughly equal proportions to care that did not. <bookmark mark='d'/> That "
            "suggests a design: make care of high value cheap, and care of low value dear, instead of one price for "
            "everything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
