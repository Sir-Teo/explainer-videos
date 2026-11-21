from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Cartels(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Coordinated effects and cartels", r"How do you find a cartel, \ and what did it cost its "
             r"buyers?", "Chapter nine. Coordinated effects and cartels.",
             lit={2006: r"the variance screen"}, scale=("firm", "market"), horizon=("a year", "a decade"))
        self.coordinated()
        self.screen()
        self.overcharge()

    def coordinated(self):
        cards = point_cards([
            (r"fewer firms", r"fewer parties to an understanding, \ and fewer to watch", GOV),
            (r"prices that can be seen", r"cheating is noticed fast, \ so it does not pay", ALDER),
            (r"small, frequent sales", r"no single order worth breaking ranks for", BIRCH),
            (r"no maverick", r"the merger may remove the one firm that kept undercutting", CARTEL),
        ], width=12.4, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"coordinated effects: \ a merger that makes tacit collusion easier", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "A merger can also do harm without the merged firm acting alone, by making it easier for the firms "
            "that remain to stop competing. Part twelve showed why collusion can sustain itself without any "
            "agreement. The guidelines ask whether the merger tips a market towards it. <bookmark mark='a'/> "
            "Fewer firms: fewer parties to an understanding, and fewer to watch. <bookmark mark='b'/> Prices "
            "everyone can see, so cheating is noticed quickly. <bookmark mark='c'/> Many small, frequent sales, so "
            "no single order is worth breaking ranks for. <bookmark mark='d'/> And the maverick: a merger that "
            "removes the one firm that kept undercutting the others can do more harm than its share suggests. "
            "The step beyond tacit coordination is an explicit cartel, which is a crime."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def screen(self):
        C = load("cartel")
        t, price, cost = np.array(C["t"]), np.array(C["price"]), np.array(C["cost"])
        a, b = C["start"], C["end"]
        ax = plane([0, 180], [45, 95], center=UP * 1.0 + LEFT * 0.4, x_length=11.0, y_length=2.9,
                   xticks=[0, 36, 72, 108, 144, 180], yticks=[50, 70, 90], ylabel=r"\$ a tonne",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        sh = shade(ax, [(a, b)], 45, 95, CARTEL, 0.12)
        pc = path(ax, t, price, WHITE, 2.2, smooth=False)
        cc = path(ax, t, cost * 1.25, GREY_B, 1.6, smooth=False).set_stroke(opacity=0.7)
        ck = VGroup(label(r"white: \ price", font_size=14, color=WHITE),
                    label(r"grey: \ cost $\times$ 1.25", font_size=14, color=GREY_B)).arrange(
            RIGHT, buff=0.4).next_to(ax.ax.c2p(0, 95), RIGHT, buff=0.1).shift(UP * 0.1)
        cv = np.array(C["cv"])
        bx = plane([0, 180], [0, 0.08], center=DOWN * 2.3 + LEFT * 0.4, x_length=11.0, y_length=1.8,
                   xticks=[0, 36, 72, 108, 144, 180], yticks=[0, 0.04, 0.08], xlabel=r"month",
                   ylabel=r"volatility", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=13)
        tt = np.arange(1, len(cv) + 1)
        cvp = path(bx, tt[12:], cv[12:], ALDER, 2.2, smooth=False)
        thr = DashedLine(bx.ax.c2p(0, C["threshold"]), bx.ax.c2p(180, C["threshold"]), color=E.ACCENT,
                         stroke_width=1.6)
        flags = VGroup(*[Dot(bx.ax.c2p(k + 1, 0.004), radius=0.035, color=CARTEL) for k in range(12, len(cv))
                         if C["flag"][k]])
        cl = label(r"the cartel, \ months 72--131", font_size=15, color=CARTEL).next_to(ax.ax.c2p((a + b) / 2, 45),
                                                                                       UP, buff=0.08)
        tag = island_tag(r"the Island: \ cement, \ a cartel planted", corner=DR, font_size=12)
        with self.voiceover(
            "Cartels are found mostly through leniency: the first member to confess escapes the fine, so cartels "
            "tend to betray themselves. Economists add screens, which look for the fingerprints of collusion in "
            "prices. <bookmark mark='a'/> Here is fifteen years of the Island's cement price, against its cost. "
            "<bookmark mark='b'/> For five of those years the producers ran a cartel. Watch what happens to the "
            "price: it sits higher above cost, and it is calmer. Agreeing on every change is costly, so cartels "
            "move prices less often and less sharply. <bookmark mark='c'/> A variance screen measures that: the "
            "volatility of the month-to-month change in the margin, over a rolling year. During the cartel it "
            f"falls from about {C['cv_outside']:.3f} to {C['cv_during']:.3f}. <bookmark mark='d'/> The months in "
            "the calmest quarter are flagged, in red. A flag is a reason to look, not proof. Rosa Abrantes-Metz and "
            "her coauthors built the screen in 2006 from a real case, a bid-rigging ring selling frozen perch to a "
            "military supply centre in Philadelphia: when the conspiracy collapsed, the price fell and its standard "
            "deviation more than doubled."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(ck))
            vo.wait_until("a")
            self.play(Create(cc), Create(pc), run_time=2.2)
            vo.wait_until("b")
            self.play(FadeIn(sh), FadeIn(cl))
            vo.wait_until("c")
            self.play(FadeIn(bx), Create(cvp), run_time=1.8)
            vo.wait_until("d")
            self.play(Create(thr), LaggedStart(*[FadeIn(f) for f in flags], lag_ratio=0.02), run_time=1.6)
        self.clear_scene()

    def overcharge(self):
        C = load("cartel")
        t, price, bf = np.array(C["t"]), np.array(C["price"]), np.array(C["but_for"])
        a, b = C["start"], C["end"]
        ax = plane([48, 156], [50, 90], center=LEFT * 2.7 + DOWN * 0.5, x_length=6.4, y_length=4.4,
                   xticks=[48, 72, 96, 120, 144], yticks=[50, 60, 70, 80, 90], xlabel=r"month",
                   ylabel=r"\$ a tonne", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        m = (t >= 48) & (t <= 156)
        pc = path(ax, t[m], price[m], WHITE, 2.4, smooth=False)
        md = (t >= a) & (t < b)
        bfc = path(ax, t[md], bf[md], SAVE, 2.4, smooth=False)
        gap = VGroup(*[Line(ax.ax.c2p(x, y0), ax.ax.c2p(x, y1), color=CARTEL, stroke_width=2).set_opacity(0.5)
                       for x, y0, y1 in zip(t[md][::2], bf[md][::2], price[md][::2])])
        side = VGroup(
            MathTex(r"\ln p_t = \alpha + \beta \ln c_t + \delta\,\text{cartel}_t + \varepsilon_t", font_size=30,
                    color=WHITE),
            label(rf"the overcharge: \ $e^{{\hat\delta}} - 1 = {100 * C['estimate']:.1f}\%$ \ "
                  rf"(s.e. {100 * C['se']:.1f}); \ planted: \ {100 * C['truth']:.0f}\%", font_size=20,
                  color=CARTEL),
            label(r"green: \ the but-for price, \ had there been no cartel", font_size=19, color=SAVE),
            label(rf"damages: \ the overcharge on every tonne bought, \\ about \${C['damages'] / 1000:.0f} million; "
                  rf"\ trebled in America: \ \${3 * C['damages'] / 1000:.0f} million", font_size=19,
                  color=E.ACCENT),
            label(r"before--during--after: \ the years outside the cartel \\ say what prices would have been",
                  font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ cement, \ quantities in thousands of tonnes a month", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Once a cartel is caught, its buyers sue, and the economist's job is the overcharge: how much higher "
            "were prices than they would have been? <bookmark mark='a'/> The workhorse is the before-during-after "
            "regression: the log price on the log cost and an indicator for the cartel months. The years outside "
            f"the cartel say how price tracks cost. <bookmark mark='b'/> Here the overcharge is "
            f"{say_pct(C['estimate'], 1)}, against the {say_pct(C['truth'], 0)} the Island planted. <bookmark "
            "mark='c'/> Dividing it out gives the but-for price, what buyers would have paid. <bookmark mark='d'/> "
            "The damages are the gap on every tonne bought: about "
            f"{C['damages'] / 1000:.0f} million dollars, and American law trebles them, to give victims a reason "
            "to sue "
            "and cartels a reason to fear it. <bookmark mark='e'/> Every choice in that regression is contestable: "
            "which months count as clean, whether costs were themselves affected, whether the cartel's end was "
            "really its end. Part twelve's Dial records how large overcharges usually are; this part adds the "
            "Island's."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(pc), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[4]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(bfc), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(g) for g in gap], lag_ratio=0.03), FadeIn(side[3]), run_time=1.6)
            vo.wait_until("e")
        self.clear_scene()
