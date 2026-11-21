from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Witness(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Regression in the witness box", r"What does a regression look like \ when the other side "
             r"has it?", "Chapter ten. Regression in the witness box.",
             lit={1993: r"Daubert", 1999: r"Kumho Tire", 2006: r"Staples revisited"},
             scale=("market",), horizon=("a year",))
        self.daubert()
        self.direct()
        self.cross()

    def daubert(self):
        hc = history_card(1993, r"Daubert v. Merrell Dow Pharmaceuticals", r"the trial judge is a gatekeeper: \ "
                          r"expert testimony must rest on a reliable method, \ reliably applied", color=E.ACCENT,
                          width=11.4, font_size=22).to_edge(UP, buff=0.5)
        cards = point_cards([
            (r"tested", r"can the method be checked, \ and has it been?", GOV),
            (r"reviewed", r"has it been published and criticized?", ALDER),
            (r"error rate", r"how often is it wrong, \ and by how much?", CARTEL),
            (r"accepted", r"do others in the field use it?", BIRCH),
        ], width=12.4, cols=4, font_size=19).next_to(hc, DOWN, buff=0.5)
        later = VGroup(
            label(r"1999, \ Kumho Tire: \ the same for every expert, \ economists included", font_size=20,
                  color=GREY_A),
            label(r"2023: \ Rule 702 amended: \ the judge must find each condition more likely than not", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(cards, DOWN, buff=0.5)
        tag = published_tag(r"509 U.S. 579 (1993); \ 526 U.S. 137 (1999); \ Federal Rule of Evidence 702",
                            corner=DL, font_size=12)
        with self.voiceover(
            "An economist in court is an expert witness, and a judge decides whether the testimony may be heard at "
            "all. <bookmark mark='a'/> In 1993, in Daubert against Merrell Dow, the Supreme Court made the trial "
            "judge a gatekeeper: expert testimony must rest on a reliable method, reliably applied. <bookmark "
            "mark='b'/> It suggested questions. Can the method be tested, and has it been? Has it been through peer "
            "review? What is its error rate? Is it accepted in the field? <bookmark mark='c'/> In 1999 the Kumho "
            "Tire case extended the gate to every kind of expert, economists included, and in 2023 the federal rule "
            "was amended to say that the judge must find each condition more likely than not. A regression that "
            "only its author could defend does not get through."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards.cards], lag_ratio=0.4),
                      run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(later[0]), FadeIn(later[1]))
        self.clear_scene()

    def direct(self):
        R = load("regression")
        T = load("towns")
        size, logp = np.array(T["size"]), np.log(np.array(T["price"]))
        birch = np.array(T["birch"], bool)
        ax = plane([-2.5, 2.5], [4.3, 4.7], center=LEFT * 2.8 + DOWN * 0.4, x_length=6.2, y_length=4.6,
                   xticks=[-2, -1, 0, 1, 2], yticks=[4.3, 4.4, 4.5, 4.6, 4.7], xlabel=r"town size \ (log population, "
                   r"standardized)", ylabel=r"log of Alder's price", xfmt=lambda v: f"{v:.0f}".replace("-", "{-}"),
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(float(np.clip(x, -2.45, 2.45)), float(np.clip(y, 4.305, 4.695))),
                           radius=0.06, color=BIRCH if b else ALDER) for x, y, b in zip(size, logp, birch)])
        full, bare = R["full"], R["bare"]
        side = VGroup(
            MathTex(r"\ln p_A = \alpha - \beta_B\,\text{Birch} - \beta_C\,\text{Cedar} + \gamma_1\,\text{cost} + "
                    r"\gamma_2\,\text{size} + \varepsilon", font_size=26, color=WHITE),
            label(rf"no controls: \ Birch lowers Alder's price {bare['birch']:.1f}\% \ (s.e. {bare['birch_se']:.1f})",
                  font_size=20, color=DEF),
            label(rf"with cost and size: \ {full['birch']:.1f}\% \ (s.e. {full['birch_se']:.1f})", font_size=20,
                  color=GOV),
            label(rf"the merger's true average effect: \ +{R['truth']:.1f}\%", font_size=20, color=WHITE),
            label(r"gold: \ towns with Birch; \ blue: \ without", font_size=16, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.6:
            side.width = 6.6
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ sixty towns, \ prices with a little noise", corner=DL, font_size=12)
        with self.voiceover(
            "First, direct examination: the agency's economist presents the price regression, as in Staples. "
            "<bookmark mark='a'/> Alder's price rises with town size, because rents do, and bigger towns are also "
            "where Birch tends to be. <bookmark mark='b'/> So regress the log of Alder's price on whether Birch and "
            f"Cedar are present. Without controls, Birch's presence lowers Alder's price by {bare['birch']:.1f} "
            "percent: the dearer rents of Birch's towns hide part of the effect. <bookmark mark='c'/> Hold costs "
            f"and size fixed, and the estimate is {full['birch']:.1f} percent, with a standard error under one. "
            f"<bookmark mark='d'/> The merger's true average effect where both chains are present is "
            f"{R['truth']:.1f} percent; losing Birch as a rival is close to what the merger does. The agency's "
            "witness says: this merger would raise Alder's prices by about ten percent where the two meet."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[4]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.02), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def cross(self):
        R = load("regression")
        W = load("witness")
        mv = sorted(R["multiverse"], key=lambda r: r["effect"])
        ax = plane([0, 17], [0, 18], center=LEFT * 2.6 + DOWN * 0.3, x_length=6.6, y_length=4.4, xticks=[],
                   yticks=[0, 3, 6, 9, 12, 15, 18], ylabel=r"Birch's effect on Alder's price, \ \%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        bars = VGroup()
        for k, r in enumerate(mv):
            x = k + 1
            col = GOV if (r["cost"] or r["size"]) else DEF
            bars.add(VGroup(Line(ax.ax.c2p(x, r["effect"] - 2 * r["se"]), ax.ax.c2p(x, r["effect"] + 2 * r["se"]),
                                 color=col, stroke_width=2),
                            Dot(ax.ax.c2p(x, r["effect"]), radius=0.06, color=col)))
        truth = DashedLine(ax.ax.c2p(0, R["truth"]), ax.ax.c2p(17, R["truth"]), color=WHITE, stroke_width=1.6)
        tl = label(rf"the truth: \ {R['truth']:.1f}", font_size=15, color=WHITE).next_to(ax.ax.c2p(17, R["truth"]),
                                                                                        UP, buff=0.05).shift(
            LEFT * 0.9)
        sub = W["subsamples"]
        side = VGroup(
            label(r"16 specifications: \ costs, \ size, \ logs, \ Cedar \ in or out", font_size=19, color=GREY_A),
            label(r"purple: \ neither cost nor size controlled", font_size=16, color=DEF),
            label(rf"range: \ {R['mv_min']:.1f} to {R['mv_max']:.1f}\%; \ every one far from zero", font_size=20,
                  color=WHITE),
            label(rf"drop any one town: \ {W['loo_min']:.1f} to {W['loo_max']:.1f}\%", font_size=20,
                  color=WHITE),
            label(rf"towns with Cedar: \ {sub['towns with Cedar']['effect']:.1f}\%; \ without: \ "
                  rf"{sub['towns without Cedar']['effect']:.1f}\%", font_size=20, color=BIRCH),
            label(r"the defence's best question: \ which towns does the average describe?", font_size=18,
                  color=DEF),
            label(r"Staples, \ 1997: \ the FTC's model 8.6\%, \ the defence's 0.9\%: \\ two models, \ built "
                  r"differently", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Ashenfelter, Ashmore, Baker, Gleason and Hosken (2006), \ International Journal of "
                            r"the Economics of Business", corner=DL, font_size=12)
        with self.voiceover(
            "Now the cross-examination. The other side has the data and the code, and will try every reasonable "
            "alternative. <bookmark mark='a'/> Sixteen specifications: costs in or out, size in or out, logs or "
            f"levels, Cedar in or out. <bookmark mark='b'/> They run from {R['mv_min']:.1f} to {R['mv_max']:.1f} "
            "percent, and every one is far from zero; the ones that leave out cost and size are lowest, for the "
            f"reason you saw. <bookmark mark='c'/> Drop any single town, and the estimate stays between "
            f"{W['loo_min']:.1f} and {W['loo_max']:.1f}. <bookmark mark='d'/> The best question is a different one: "
            f"which towns does the average describe? Where Cedar is present, Birch's effect is only "
            f"{sub['towns with Cedar']['effect']:.1f} percent; where it is absent, "
            f"{sub['towns without Cedar']['effect']:.1f}. <bookmark mark='e'/> That is a fair point, and an honest "
            "witness concedes it and says what it implies: the harm is concentrated in the towns without Cedar, "
            "which is where a remedy would have to sell stores. <bookmark mark='f'/> In the real case the FTC's "
            "model predicted prices 8.6 percent higher and the defence's 0.9. Ashenfelter and his coauthors later "
            "traced the gap to the differences in how the two models were built, and the judge had found the FTC's "
            "evidence the more persuasive. The lesson is to put the alternatives on the table yourself, before the "
            "other side does."
        ) as vo:
            self.play(FadeIn(ax), Create(truth), FadeIn(tl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.08),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
            vo.wait_until("f")
            self.play(FadeIn(side[6]))
        self.clear_scene()
