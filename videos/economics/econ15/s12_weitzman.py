from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403

TAXC = "#7BD88F"
QUOTAC = "#C9A0FF"


def panel(case, center, title, b0=10.0, c0=2.0):
    bb, cc = case["mb_slope"], case["mc_slope"]
    ax = plane([0, 6.5], [0, 13], center=center, x_length=5.2, y_length=3.7, xticks=[], yticks=[],
               xlabel=r"tonnes cut", ylabel=r"\$ a tonne", font_size=14)
    a = ax.ax
    qs = np.linspace(0, 6.5, 60)
    mb = path(ax, qs, b0 - bb * qs, color=DEMAND, width=3, smooth=False, yr=(0, 13))
    mcs = VGroup(*[path(ax, qs, c0 + th + cc * qs, color=SOCIAL, width=2 if th else 3, smooth=False, yr=(0, 13))
                   for th in (-1.0, 0.0, 1.0)])
    mcs[0].set_stroke(opacity=0.5)
    mcs[2].set_stroke(opacity=0.5)
    tax = seg(ax, 0, case["tax"], 6.5, case["tax"], color=TAXC, width=2.5, dashed=True)
    quota = seg(ax, case["q_bar"], 0, case["q_bar"], 13, color=QUOTAC, width=2.5, dashed=True)
    t = label(title, font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1)
    nums = VGroup(label(rf"expected loss with the tax: \ {case['loss_tax']:.4g}", font_size=16, color=TAXC),
                  label(rf"with the quota: \ {case['loss_quota']:.4g}", font_size=16, color=QUOTAC)
                  ).arrange(DOWN, buff=0.08).next_to(ax, DOWN, buff=0.15)
    return VGroup(ax, mb, mcs, tax, quota, t, nums)


class Weitzman(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Prices or quantities?", r"When the cost of cutting pollution is uncertain, \ is a tax better than "
             r"a cap?", "Chapter ten. Prices or quantities?",
             lit={1974: r"Weitzman", 1976: r"Roberts and Spence", 2002: r"Pizer on carbon"},
             scale=("market", "nation"), horizon=("a year",))
        self.setup_()
        self.panels()
        self.carbon()

    def setup_(self):
        rows = VGroup(
            label(r"with perfect knowledge, \ a tax and a cap do the same: \ set either, \ get the other", font_size=24),
            label(r"but the regulator must choose before it knows what cutting will cost", font_size=24, color=SOCIAL),
            label(r"a tax fixes the price, \ and lets the quantity cut move with the costs", font_size=24, color=TAXC),
            label(r"a cap fixes the quantity, \ and lets the price move", font_size=24, color=QUOTAC),
            label(r"Martin Weitzman, \ 1974: \ which mistake is cheaper depends on two slopes", font_size=25,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Weitzman, RES 41(4) (1974)", corner=DR, font_size=13)
        with self.voiceover(
            "Pigou sets a price; Dales sets a quantity. Does it matter which? <bookmark mark='a'/> With perfect "
            "knowledge, no: set the right tax and the market cuts the right amount; set the right cap and the market "
            "finds the right price. <bookmark mark='b'/> But a regulator must choose before it knows what cutting "
            "will cost. <bookmark mark='c'/> A tax fixes the price, and lets the amount cut move with the costs. "
            "<bookmark mark='d'/> A cap fixes the amount, and lets the price move. <bookmark mark='e'/> In 1974 "
            "Martin Weitzman showed that which mistake is cheaper depends on two slopes: how fast the benefit of "
            "cutting falls, and how fast its cost rises."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def panels(self):
        w = load("weitzman")
        left = panel(w["cases"][0], LEFT * 3.5 + UP * 0.2, r"flat benefit, \ steep cost")
        right = panel(w["cases"][1], RIGHT * 3.5 + UP * 0.2, r"steep benefit, \ flat cost")
        key = VGroup(
            label(r"benefit of cutting", font_size=15, color=DEMAND),
            label(r"cost of cutting: \ expected, \ and if luck runs either way", font_size=15, color=SOCIAL),
            label(r"the tax", font_size=15, color=TAXC), label(r"the cap", font_size=15, color=QUOTAC),
        ).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.3)
        foot = label(r"set a price when cost is steeper than benefit; \ set a quantity when benefit is steeper",
                     font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Weitzman (1974); \ the numbers: \ Agora", corner=DR, font_size=12)
        with self.voiceover(
            "Here are the two cases, with the same uncertainty about cost. The red lines are the expected cost of "
            "cutting, and what it turns out to be if luck runs either way. <bookmark mark='a'/> On the left, the "
            "benefit of cutting falls slowly, and the cost rises steeply. If costs turn out high, a cap forces "
            "expensive cuts whose benefit is barely above the expected; a tax lets firms cut less, which costs "
            "little since the benefit is flat. The tax's expected loss is a sixteenth of the cap's. "
            "<bookmark mark='b'/> On the right, the benefit falls steeply: there is a threshold, past which damage "
            "mounts fast. Now a tax risks too little cutting exactly where it matters, and the cap's expected loss "
            "is a sixteenth of the tax's. <bookmark mark='c'/> The rule: set a price when the cost curve is steeper "
            "than the benefit curve, and a quantity when the benefit curve is steeper."
        ) as vo:
            self.play(FadeIn(key), FadeIn(tag), FadeIn(left[0]), FadeIn(right[0]), FadeIn(left[5]), FadeIn(right[5]))
            self.play(*[Create(p_[1]) for p_ in (left, right)], *[Create(p_[2]) for p_ in (left, right)], run_time=2)
            vo.wait_until("a")
            self.play(Create(left[3]), Create(left[4]), FadeIn(left[6]))
            vo.wait_until("b")
            self.play(Create(right[3]), Create(right[4]), FadeIn(right[6]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def carbon(self):
        rows = VGroup(
            label(r"carbon dioxide does its damage as a stock, \ built up over decades", font_size=24),
            label(r"one more year's tonne barely changes the stock: \ the benefit of cutting it is nearly flat",
                  font_size=24, color=DEMAND),
            label(r"so for carbon, \ Weitzman's rule favours a price \ (William Pizer, \ 2002)", font_size=24,
                  color=TAXC),
            label(r"a hybrid: \ a cap with a ceiling and a floor on the permit's price \ (Roberts and Spence, \ 1976)",
                  font_size=23, color=QUOTAC),
            label(r"part forty-eight takes up climate", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Pizer, J. Public Econ. 85(3) (2002); \ Roberts and Spence, J. Public Econ. 5 (1976)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "The rule has a famous application. <bookmark mark='a'/> Carbon dioxide does its damage as a stock, "
            "built up over decades. <bookmark mark='b'/> One more year's tonne barely changes the stock, so the "
            "benefit of cutting it is nearly flat. <bookmark mark='c'/> By Weitzman's rule, that favours a price, as "
            "William Pizer found in 2002. <bookmark mark='d'/> There are hybrids too: a cap with a ceiling and a "
            "floor on the permit's price, which Marc Roberts and Michael Spence proposed in 1976, and which several "
            "carbon markets now use. <bookmark mark='e'/> Part forty-eight takes up climate in full."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
