from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403


class Market(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Market structure", r"Scale, \ data and compute: \ will a few firms capture the gains?",
             "Chapter ten. Market structure.", scale=("market", "world"), horizon=("a year", "a decade"))
        self.costs()
        self.entry()
        self.chain()

    def costs(self):
        cards = point_cards([
            (r"a fixed cost", r"training a frontier model: \ months on tens of thousands of chips; \ the compute "
             r"used to train frontier models has grown four to five times a year since 2010", NAIVE),
            (r"a small marginal cost", r"serving one more answer costs little, \ and the price of a given level "
             r"of capability has fallen fast", NEWT),
            (r"economies of scale", r"a cost that is mostly fixed favours a few large producers: \ Part 10's "
             r"natural monopoly, \ Part 44's platforms", MACH),
            (r"and against them", r"followers learn from leaders' outputs, \ open-weight models are free to run, "
             r"\ and users switch easily between models", GDP),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"the cost structure of a model", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Epoch AI, \ training compute of notable models (2024); \ Korinek and Vipra, \ "
                            r"Economic Policy 40(121) (2025)", corner=DL, font_size=12)
        with self.voiceover(
            "Who will capture the gains? Start with costs. <bookmark mark='a'/> Training a frontier model is an "
            "enormous fixed cost: months of computation on tens of thousands of chips. Epoch AI's records show the "
            "compute used to train frontier models growing four to five times a year since 2010. <bookmark mark='b'/> "
            "Serving one more answer costs little, and the price of a given level of capability has fallen fast. "
            "<bookmark mark='c'/> A cost that is mostly fixed favours a few large producers: the natural monopoly of "
            "Part ten, and the platforms of Part forty-four. <bookmark mark='d'/> But there are forces the other way. "
            "Followers can learn from the leaders' outputs, open-weight models can be run by anyone, and users switch "
            "between models with a click. Anton Korinek and Jai Vipra map these forces in detail."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def entry(self):
        E_ = load("entry")
        t = np.array(E_["t"])
        axl = plane([-0.5, len(t) - 0.5], [-1, 4], center=LEFT * 3.4 + DOWN * 0.3, x_length=5.8, y_length=4.4,
                    xticks=list(range(0, len(t), 2)), yticks=[-1, 0, 1, 2, 3, 4], xlabel=r"years",
                    ylabel=r"size, \ log scale", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"10^{{{v:.0f}}}",
                    font_size=13)
        ml = path(axl, t, np.log10(E_["market"]), NEWT, 3.0, smooth=False)
        cl = path(axl, t, np.log10(E_["cost"]), NAIVE, 3.0, smooth=False)
        key = legend_rows([(NEWT, "the market: doubles each year"), (NAIVE, "a frontier model's cost: triples")],
                          font_size=14).next_to(axl.ax.c2p(-0.5, 4), DR, buff=0.15)
        axr = plane([-0.5, len(t) - 0.5], [0, 10], center=RIGHT * 3.4 + DOWN * 0.3, x_length=5.8, y_length=4.4,
                    xticks=list(range(0, len(t), 2)), yticks=[0, 2, 4, 6, 8, 10], xlabel=r"years",
                    ylabel=r"frontier firms that can cover the cost", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:.0f}", font_size=13)
        nb = bars(axr, t, E_["n"], [MACH] * len(t), width=0.6)
        eq = MathTex(r"\pi = \frac{M}{(N+1)^2} \geq F \;\Rightarrow\; N^\ast = \sqrt{M/F} - 1",
                     font_size=32).to_edge(UP, buff=0.35)
        tag = island_tag(r"a toy: \ Cournot competition with free entry; \ agora.automation.frontier\_entry",
                         corner=DL, font_size=12)
        with self.voiceover(
            "A toy makes the arithmetic plain. <bookmark mark='a'/> With Cournot competition on a linear demand, "
            "each of N firms earns the market size M over N plus one squared. Entry stops when that no longer "
            "covers the fixed cost F of a frontier model: at about the square root of M over F, minus one. "
            "<bookmark mark='b'/> Suppose the market doubles each year, but the cost of staying at the frontier "
            f"triples. <bookmark mark='c'/> The market supports {E_['n'][0]} frontier firms in the first year, "
            f"{E_['n'][3]} after three years, and {E_['n'][-1]} by the end. If the cost of the frontier grows "
            "faster than the market for it, the frontier narrows to a very few firms. Below it, a competitive "
            "layer of older and open models, priced near cost. These are invented numbers. The point is the race "
            "between two growth rates, which the industry's next few years will measure."
        ) as vo:
            self.play(FadeIn(axl), FadeIn(axr), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(Create(ml), Create(cl), FadeIn(key), run_time=1.8)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in nb], lag_ratio=0.12), run_time=2.0)
        self.clear_scene()

    def chain(self):
        ch = flow_chain([(r"chips", NAIVE), (r"data centres and cloud", GDP), (r"model makers", MACH),
                         (r"applications", TEXT), (r"users and workers", WORK)], box_w=2.25, box_h=1.0,
                        font_size=17).move_to(UP * 1.6)
        rows = VGroup(
            label(r"who captures the surplus? \ whoever is scarcest along the chain", font_size=21,
                  color=E.ACCENT),
            label(r"today: \ chips and power are scarce; \ models compete, \ and prices of a given capability "
                  r"fall", font_size=19, color=GREY_A),
            label(r"if models stay close to one another, \ most of the gains pass to users, \ as a consumer "
                  r"surplus GDP does not count \ (Part 3)", font_size=19, color=WORK),
            label(r"if one model pulls ahead, \ or owns the data and the customers, \ Part 44's questions return",
                  font_size=19, color=NAIVE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(ch, DOWN, buff=0.7)
        if rows.width > 12.8:
            rows.scale_to_fit_width(12.8)
        with self.voiceover(
            "AI is made along a chain. <bookmark mark='a'/> Chips, data centres, the model makers, the "
            "applications built on the models, and finally users and workers. <bookmark mark='b'/> The surplus goes "
            "to whoever is scarcest along the chain. <bookmark mark='c'/> Today, chips and electricity are "
            "scarce, and models compete hard, so the price of a given capability keeps falling. <bookmark "
            "mark='d'/> If models stay close to one another, most of the gains pass to the people who use them, "
            "as consumer surplus, much of which GDP does not count: Part three's free goods. <bookmark mark='e'/> "
            "If one model pulls far ahead, or owns the data and the customers, the questions of Part forty-four, "
            "lock-in, tying and self-preferencing, return at a larger scale."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in ch.boxes], lag_ratio=0.2),
                      LaggedStart(*[Create(a) for a in ch.arrows], lag_ratio=0.2), run_time=2.0)
            for mk, r_ in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()
