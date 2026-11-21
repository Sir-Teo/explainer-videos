from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Addiction(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Addiction", r"Can an addict be choosing?", "Chapter twelve. Addiction.",
             lit={1988: r"Becker and Murphy", 2001: r"Gruber and Kőszegi"}, scale=("person", "nation"),
             horizon=("a year", "a lifetime"))
        self.model()
        self.paths()
        self.cigarettes()
        self.test()

    def model(self):
        rows = VGroup(
            label(r"past use builds a stock: \ tolerance and habit", font_size=24, color=DRUG),
            label(r"the stock makes more use pleasurable now \ (reinforcement)", font_size=24, color=WHITE),
            label(r"and does harm later \ (to health, \ work, \ family)", font_size=24, color=LOSS),
            label(r"a rational addict weighs both, \ looking ahead", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.5)
        eq = MathTex(r"u(c_t, S_t), \qquad S_{t+1} = (1-\delta)\,S_t + c_t", font_size=36,
                     color=THEORY).to_edge(DOWN, buff=1.0)
        tag = published_tag(r"Becker and Murphy, \ JPE (1988)", corner=DR, font_size=11)
        with self.voiceover(
            "Addiction looks like the opposite of choice. In 1988 Becker and Kevin Murphy argued that it could be "
            "chosen anyway. <bookmark mark='a'/> Past use builds a stock, of tolerance and habit. <bookmark "
            "mark='b'/> The stock makes more use more rewarding now: this is what makes a good addictive. <bookmark "
            "mark='c'/> And it does harm later, to health, to work, to family. <bookmark mark='d'/> A rational "
            "addict, in their model, sees all of this and still chooses to use, because the pleasure now is worth "
            "the cost later to them. <bookmark mark='e'/> The model's sharpest prediction is about the future: if "
            "the price of a drug will rise next year, a rational addict cuts back now."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]), run_time=1.0)
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            self.play(Write(eq), run_time=1.5)
            vo.wait_until("e")
            self.play(Indicate(eq, color=WHITE), Indicate(rows[3], color=WHITE, scale_factor=1.03))
        self.clear_scene()

    def paths(self):
        A = load("addiction")
        t = np.array(A["t"])
        ax = plane([0, 40], [0, 3.2], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.4,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 1, 2, 3], xlabel=r"period", ylabel=r"use per period",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        rat = path(ax, t, A["rational"], E.ACCENT, 3.4, smooth=False)
        myo = path(ax, t, A["myopic"], DRUG, 3.4, smooth=False)
        ann = vline(ax, A["announce_at"], 0, 3.2, GREY_B)
        ann_l = label(r"rise announced", font_size=15, color=GREY_B).next_to(ax.ax.c2p(A["announce_at"], 3.1), RIGHT,
                                                                               buff=0.08)
        rise = vline(ax, A["rise_at"], 0, 3.2, LOSS)
        rise_l = label(rf"price \ {A['price0']:.1f} $\to$ {A['price1']:.1f}", font_size=15, color=LOSS).next_to(
            ax.ax.c2p(A["rise_at"], 2.9), RIGHT, buff=0.08)
        side = VGroup(
            label(r"purple: \ myopic, \\ ignores the stock's \\ future effects", font_size=17, color=DRUG),
            label(r"gold: \ rational, \\ counts them", font_size=17, color=E.ACCENT),
            label(rf"before the rise: \\ myopic {100 * A['myopic_drop_before']:+.0f}\%, \\ rational "
                  rf"{100 * A['rational_drop_before']:+.0f}\%".replace("-", "{-}"), font_size=17, color=WHITE),
            label(r"the rational addict \\ starts cutting back \\ when the news comes", font_size=17, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Two Island users of an addictive good, starting from nothing. <bookmark mark='a'/> The myopic one "
            "ignores how today's use will shape tomorrow's cravings and harms; use climbs as the habit builds. "
            "<bookmark mark='b'/> The rational one counts those effects, and settles at a lower level. <bookmark "
            f"mark='c'/> At period {A['announce_at']}, a price rise is announced, to take effect ten periods later. "
            f"<bookmark mark='d'/> The myopic user carries on climbing, {100 * A['myopic_drop_before']:+.0f} "
            "percent before the rise. The rational user starts cutting back at once, "
            f"{100 * abs(A['rational_drop_before']):.0f} percent before the price has changed, because cutting "
            "back now leaves a smaller habit to feed when the price is high. <bookmark mark='e'/> When the rise "
            "comes, both cut sharply, and the rational addict's long-run response is the larger."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(myo), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(rat), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(ann), FadeIn(ann_l))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]), Indicate(rat, color=WHITE))
            vo.wait_until("e")
            self.play(Create(rise), FadeIn(rise_l))
        self.clear_scene()

    def cigarettes(self):
        C = load("cigarettes")
        lp, lq = np.array(C["lp"]), np.array(C["lq"])
        ax = plane([4.5, 5.1], [3.85, 5.2], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.4,
                   xticks=[4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1], yticks=[4.0, 4.25, 4.5, 4.75, 5.0],
                   xlabel=r"log real price a pack, \ 1995", ylabel=r"log packs a head, \ 1995",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.05, color=DRUG) for a, b in zip(lp, lq)])
        b, se, F = C["cross"]
        mx, my = float(lp.mean()), float(lq.mean())
        fit = seg(ax, 4.55, my + b * (4.55 - mx), 5.08, my + b * (5.08 - mx), E.ACCENT, 3.2)
        rows = VGroup(
            label(rf"least squares: \ {C['ols']:.2f}".replace("-", "{-}"), font_size=17, color=GREY_A),
            label(rf"instrument, \ the sales tax: \\ {b:.2f} \ (s.e. {se:.2f}; \ $F$ {F:.0f})".replace("-", "{-}"),
                  font_size=17, color=E.ACCENT),
            label(rf"ten-year changes, \\ both taxes: \ {C['diff_both'][0]:.2f} \\ (s.e. {C['diff_both'][1]:.2f})"
                  .replace("-", "{-}"), font_size=17, color=GAIN),
            label(r"addicts respond to price: \\ about one for one", font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"The Tax Burden on Tobacco, \ via Stock and Watson and AER; \ estimated here", corner=DL,
                       font_size=12)
        with self.voiceover(
            "Do addicts respond to prices at all? <bookmark mark='a'/> Here are the forty-eight continental states "
            "in 1995, cigarettes smoked per head against the real price of a pack. Prices differ mostly because "
            "taxes differ. <bookmark mark='b'/> A simple regression gives an elasticity of "
            f"{say_num(C['ols'], 2)}. But price and consumption are set together, so use the general sales tax, "
            "which moves the price of cigarettes for reasons unrelated to smoking, as an instrument: <bookmark "
            f"mark='c'/> {say_num(b, 2)}. <bookmark mark='d'/> Over ten years, from 1985 to 1995, with both the "
            f"sales tax and the tax on cigarettes as instruments: {say_num(C['diff_both'][0], 2)}. These are the "
            "textbook estimates of Stock and Watson, reproduced here. <bookmark mark='e'/> Smokers are addicted, "
            "and smokers respond to price, about one for one in the long run. Both are true."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(fit), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def test(self):
        cards = point_cards([
            (r"the test", r"do smokers cut back \\ when a tax rise is \\ announced, \ before \\ it bites?", DRUG),
            (r"Gruber and Kőszegi", r"yes: \ forward-looking, \\ as Becker and \\ Murphy predicted", GAIN),
            (r"but", r"time-inconsistent \\ smokers, \ who plan \\ to quit and don't, \\ fit as well", HOLD),
            (r"and so", r"the welfare advice \\ flips: \ a tax helps \\ them keep their \\ own plans", E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"rational, \ or forward-looking?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.ADDICTION_49.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Jonathan Gruber and Botond Kőszegi put the sharpest prediction to the data. <bookmark mark='a'/> When "
            "cigarette tax rises were announced in advance, did smoking fall before they took effect? <bookmark "
            "mark='b'/> It did: smokers are forward-looking. <bookmark mark='c'/> But the same evidence fits "
            "smokers who are forward-looking and present-biased, like the gym members of Part forty-five, who plan "
            "to quit and keep putting it off. <bookmark mark='d'/> And the difference matters. For Becker's rational "
            "addict, a tax only costs the smoker. For the present-biased one, a tax helps them do what they "
            "themselves wanted to do, and the right tax is much higher. The model survives the test; its welfare "
            "advice does not, necessarily."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(cards.cards[0], color=WHITE, scale_factor=1.04))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
