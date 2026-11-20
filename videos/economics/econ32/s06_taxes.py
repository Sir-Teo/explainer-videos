from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class Taxes(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Tax changes: \ the narrative record", r"What does a tax increase do to output?",
             "Chapter five. Tax changes: the narrative record.", lit={2010: r"Romer and Romer"}, scale=("nation",),
             horizon=("a quarter", "three years"))
        self.record()
        self.response()

    def record(self):
        T = load("taxes")
        ax = plane([1945, 2009], [-3, 2], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.6,
                   xticks=[1950, 1960, 1970, 1980, 1990, 2000], yticks=[-3, -2, -1, 0, 1, 2],
                   ylabel=r"tax change, \ \% of GDP", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        zero = seg(ax, 1945, 0, 2009, 0, GREY_C, 1.5)

        def stick(t, v, col):
            return Line(ax.ax.c2p(t, 0), ax.ax.c2p(t, v), color=col, stroke_width=4)

        exo = VGroup(*[stick(t, v, GREY_B) for t, v in T["events"]])
        endo = VGroup(*[stick(t, v, GREY_B) for t, v in T["endog"]])
        side = VGroup(
            label(r"every postwar federal tax law, \\ by the quarter it took effect", font_size=18, color=GREY_A),
            label(r"Christina and David Romer read \\ every tax law's record", font_size=18, color=E.ACCENT),
            label(r"kept: \ changes made for long-run \\ reasons, \ or to pay off a deficit \\ already there",
                  font_size=18, color=TAX),
            label(r"dropped: \ changes made because \\ the economy was weak or strong", font_size=18, color=GREY_B),
            label(rf"{T['n_changes']} quarters kept: \ gold up, \ green down", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Romer and Romer, \ \emph{AER} 100(3) (2010), \ via Ramey's Handbook data", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Taxes have the same problem: governments cut taxes in recessions. <bookmark mark='a'/> Christina and "
            "David Romer read the record behind every postwar American tax law, the speeches, the committee "
            "reports, the president's messages, to learn why each was passed. <bookmark mark='b'/> They kept the "
            "changes made for long-run reasons, to promote growth or because of a view about the size of "
            "government, or to pay off a deficit already there. <bookmark mark='c'/> They dropped changes made "
            "because the economy was weak or strong, or to pay for a war. <bookmark mark='d'/> What is left, in "
            "percent of GDP: gold for increases, green for cuts."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(side[0]),
                      LaggedStart(*[Create(s_) for s_ in [*exo, *endo]], lag_ratio=0.02), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), *[s_.animate.set_color(TAX if v > 0 else OUTPUT)
                                         for s_, (t, v) in zip(exo, T["events"])])
            vo.wait_until("c")
            self.play(FadeIn(side[3]), endo.animate.set_opacity(0.12))
            vo.wait_until("d")
            self.play(FadeIn(side[4]), FadeOut(endo))
        self.clear_scene()

    def response(self):
        T = load("taxes")
        h = np.array(T["h"])
        ax = plane([0, 16], [-3.5, 0.5], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[0, 4, 8, 12, 16], yticks=[-3, -2, -1, 0], xlabel=r"quarters after the tax increase",
                   ylabel=r"real GDP, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}" if v else "0",
                   font_size=15)
        zero = seg(ax, 0, 0, 16, 0, GREY_C, 1.5)
        line = path(ax, h, T["resp"], TAX, 3.5)
        side = VGroup(
            label(r"a tax increase of 1\% of GDP", font_size=19, color=TAX),
            label(rf"this film's local projections: \\ {T['trough']:+.1f}\% after {T['trough_h']} quarters",
                  font_size=19, color=TAX),
            label(r"the Romers: \ nearly $-3\%$ \\ over three years", font_size=19, color=E.ACCENT),
            label(r"a tax multiplier of 2 to 3, \\ larger than most spending multipliers", font_size=19,
                  color=WHITE),
            label(r"why, \ when theory says the opposite, \\ is still argued", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Romer and Romer, \ \emph{AER} 100(3) (2010); \ Ramey, \ \emph{Handbook of "
                            r"Macroeconomics} 2A (2016); \ this film", corner=DR, font_size=12)
        with self.voiceover(
            "What followed? <bookmark mark='a'/> Project real GDP on the exogenous changes, quarter by quarter "
            "after a tax increase of one percent of GDP. <bookmark mark='b'/> Output falls slowly, and by "
            f"{abs(T['trough']):.1f} percent after {T['trough_h']} quarters on this film's estimate. "
            "<bookmark mark='c'/> The Romers' own estimate was a fall of nearly three percent over three years. "
            "<bookmark mark='d'/> A tax multiplier of two to three is larger than most estimates for spending, "
            "which is the opposite of what the simple Keynesian cross predicts. <bookmark mark='e'/> Part of the "
            "answer may be that taxes change incentives to work and invest, and much of the effect in their data "
            "came through investment; why the gap is so large is still argued."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(side[0]), run_time=0.6)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]), run_time=2)
            for mk, s_ in zip("cde", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
        self.clear_scene()
