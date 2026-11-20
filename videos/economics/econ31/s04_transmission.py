from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


def box(text, color, w=3.0, h=0.85, fs=19):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=2.2,
                         fill_color=color, fill_opacity=0.14)
    t = wrapped_label(text, w - 0.3, fs, WHITE)
    if t.height > h - 0.15:
        t.height = h - 0.15
    g = VGroup(r, t.move_to(r))
    g.rect = r
    return g


class Transmission(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Transmission: \ from one overnight rate to the economy", r"How does an overnight rate "
             r"reach a mortgage, \ a factory and a price?", "Chapter three. Transmission: from one overnight rate "
             "to the economy.", lit={1961: r"Friedman's lags"}, scale=("household", "firm", "nation"),
             horizon=("a day", "two years"))
        self.channels()
        self.expectations()

    def channels(self):
        src = box(r"the overnight rate", RATE, w=2.6, h=1.1, fs=22).move_to(LEFT * 5.2 + UP * 0.2)
        names = [(r"rates on loans and bonds: \ borrowing costs more", BOND),
                 (r"credit: \ banks lend less, \ to riskier borrowers least", OUTPUT),
                 (r"asset prices: \ houses and shares fall; \ wealth shrinks", PRICE),
                 (r"the exchange rate: \ the currency rises; \ exports suffer", CB),
                 (r"expectations: \ of future rates and of inflation", E.ACCENT)]
        mids = VGroup(*[box(t, c, w=4.4, h=0.82, fs=18) for t, c in names]).arrange(DOWN, buff=0.22).move_to(
            LEFT * 0.6 + UP * 0.2)
        dst1 = box(r"spending: \ homes, \ machines, \ cars, \ exports", OUTPUT, w=2.8, h=1.1, fs=19).move_to(
            RIGHT * 3.6 + UP * 1.3)
        dst2 = box(r"output and jobs first; \ prices later", INFL, w=2.8, h=1.1, fs=19).move_to(
            RIGHT * 3.6 + DOWN * 0.9)
        arr1 = VGroup(*[Arrow(src.get_right(), m.get_left(), buff=0.08, stroke_width=2.5, color=GREY_B,
                              max_tip_length_to_length_ratio=0.08) for m in mids])
        arr2 = VGroup(*[Arrow(m.get_right(), dst1.get_left(), buff=0.08, stroke_width=2.5, color=GREY_B,
                              max_tip_length_to_length_ratio=0.08) for m in mids])
        arr3 = Arrow(dst1.get_bottom(), dst2.get_top(), buff=0.08, stroke_width=3, color=GREY_A)
        top = label(r"how one overnight rate reaches the whole economy", font_size=26, color=E.ACCENT).to_edge(UP,
                                                                                                      buff=0.45)
        foot = label(r"Friedman: \ ``long and variable lags'' \ $\cdot$ \ a year or more for output, \ longer for "
                     r"prices", font_size=21, color=HOLD).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Friedman, \ \emph{JPE} 69(5) (1961); \ Mishkin, \ \emph{The Economics of Money, Banking "
                            r"and Financial Markets}", corner=DR, font_size=12)
        with self.voiceover(
            "A central bank sets one price: the rate on overnight loans between banks. How does that reach a "
            "family buying a house, or a firm deciding on a factory? Through several channels at once. "
            "<bookmark mark='a'/> Rates on longer loans and bonds move with the overnight rate and with what "
            "markets expect it to be. <bookmark mark='b'/> Banks lend less, and least to riskier borrowers. "
            "<bookmark mark='c'/> Prices of houses and shares fall, and people who feel poorer spend less. "
            "<bookmark mark='d'/> The currency rises, which makes exports dearer abroad. <bookmark mark='e'/> And "
            "expectations, of future rates and of inflation, shift at once. <bookmark mark='f'/> All of them end in "
            "spending, <bookmark mark='g'/> which moves output and jobs first and prices later. "
            "<bookmark mark='h'/> Milton Friedman called the delays long and variable: a year or more before output "
            "responds fully, longer for prices. That is why a central bank must act on forecasts, which is the root "
            "of everything hard in this part."
        ) as vo:
            self.play(FadeIn(src), FadeIn(tag), FadeIn(top))
            for mk, m, a in zip("abcde", mids, arr1):
                vo.wait_until(mk)
                self.play(GrowArrow(a), FadeIn(m, shift=RIGHT * 0.1), run_time=0.8)
            vo.wait_until("f")
            self.play(LaggedStart(*[GrowArrow(a) for a in arr2], lag_ratio=0.15), FadeIn(dst1), run_time=1.2)
            vo.wait_until("g")
            self.play(GrowArrow(arr3), FadeIn(dst2))
            vo.wait_until("h")
            self.play(FadeIn(foot))
        self.clear_scene()

    def expectations(self):
        T = load("transmission")
        t = np.array(T["t"])
        ax = plane([2021, 2024.5], [0, 6], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[2021, 2022, 2023, 2024], yticks=[0, 1, 2, 3, 4, 5, 6], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        ff = path(ax, t, T["ff"], RATE, 3.5, smooth=False)
        y2 = path(ax, t, T["y2"], PRICE, 3, smooth=False)
        y10 = path(ax, t, T["y10"], BOND, 3, smooth=False)
        hike = vline(ax, 2022.21, 0, 6, RATE, 2)
        side = VGroup(
            label(r"pink: \ the federal funds rate \\ (top of its range)", font_size=18, color=RATE),
            label(r"gold: \ the 2-year Treasury yield", font_size=18, color=PRICE),
            label(r"purple: \ the 10-year yield", font_size=18, color=BOND),
            label(rf"before the first rise, \ March 2022, \\ the 2-year yield was already {T['y2_mar22']:.1f}\%",
                  font_size=18, color=E.ACCENT),
            label(r"markets moved on the \\ expected path, \ not the rate", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Federal Reserve Board: \ H.15, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "The expectations channel can be seen directly. Here is the tightening of 2022. <bookmark mark='a'/> In "
            "pink, the top of the federal funds rate's range: zero point two five percent until March 2022, then "
            f"up to {T['ff_dec22']:.1f} by December. <bookmark mark='b'/> In gold, the two-year Treasury yield. It "
            f"began to climb in the autumn of 2021, from {T['y2_sep21']:.2f} percent in September to "
            f"{T['y2_mar22']:.1f} by March, <bookmark mark='c'/> before the Federal Reserve had raised its rate at "
            "all. <bookmark mark='d'/> The ten-year yield followed. <bookmark mark='e'/> Markets price the path "
            "they expect, so a central bank that is believed moves borrowing costs before it moves its own rate."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(ff), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(y2), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(hike), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Create(y10), FadeIn(side[2]), run_time=1.4)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
