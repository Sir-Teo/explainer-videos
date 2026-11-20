from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ policy staff and rates strategists", r"Who does this for a living, \ and "
             r"what do they do all day?", "Chapter fifteen. In practice: policy staff and rates strategists.",
             lit={2000: r"Romer and Romer"}, scale=("firm", "nation"), horizon=("a day", "a year"))
        self.jobs()
        self.called()

    def jobs(self):
        rows = VGroup(
            label(r"inside the central bank", font_size=27, color=E.ACCENT),
            label(r"the forecast round: \ every number in the Greenbook (now the Tealbook), \ before each meeting",
                  font_size=21, color=CB),
            label(r"alternative scenarios; \ rules' prescriptions with the data of the day; \ the model of Part 30",
                  font_size=21, color=CB),
            label(r"on the trading floors", font_size=27, color=E.ACCENT),
            label(r"rates strategists: \ the path the market prices, \ against the path the bank signals", font_size=21,
                  color=BOND),
            label(r"every word of a statement read for change: \ the tantrum is the job's nightmare", font_size=21,
                  color=BOND),
            label(r"both sides use the tools of this part: \ shocks, \ responses, \ real-time data, \ r$^*$",
                  font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Federal Reserve Bank of Philadelphia, \ the Tealbook data set", corner=DR, font_size=12)
        with self.voiceover(
            "Who does this work? <bookmark mark='a'/> Inside a central bank, staff economists run the forecast "
            "round. <bookmark mark='b'/> Before every meeting of the Federal Open Market Committee they produce a "
            "complete forecast, once called the Greenbook for its cover and now the Tealbook. "
            "<bookmark mark='c'/> They add alternative scenarios, the prescriptions of several rules with the "
            "data of the day, and simulations with models like Part 30's. <bookmark mark='d'/> Outside, on the "
            "trading floors of banks and funds, <bookmark mark='e'/> rates strategists compare the path of rates "
            "that markets price with the path the central bank signals, <bookmark mark='f'/> and read every "
            "statement for each changed word. <bookmark mark='g'/> Both sides use the tools of this part: shocks "
            "and their effects, real-time data, and an estimate of the neutral rate that nobody trusts very far."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcdefg", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["romer_2000"]
        K = load("called")
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=17).to_edge(UP, buff=0.3)
        ax = plane([0, 5], [0, 2], center=DOWN * 1.45 + LEFT * 1.6, x_length=7.0, y_length=2.6,
                   xticks=[], yticks=[0, 0.5, 1.0, 1.5, 2.0], ylabel=r"typical error, \ points of inflation",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        bars, labs = VGroup(), VGroup()
        for k, (era, x0) in enumerate((("rr", 0.6), ("after", 2.9))):
            for j, (key, col) in enumerate((("rmse_gb", CB), ("rmse_spf", PRICE))):
                v = K[era][key]
                p0, p1 = ax.ax.c2p(x0 + j * 0.8, 0), ax.ax.c2p(x0 + j * 0.8 + 0.7, v)
                bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.85,
                                   stroke_width=0).move_to((p0 + p1) / 2))
                labs.add(label(f"{v:.2f}", font_size=15, color=col).next_to(bars[-1], UP, buff=0.06))
        eras = VGroup(label(rf"{K['rr']['first'][:4]}--{K['rr']['last'][:4]}", font_size=16, color=GREY_A).next_to(
            ax.ax.c2p(1.35, 0), DOWN, buff=0.12),
                      label(rf"{K['after']['first'][:4]}--{K['after']['last'][:4]}", font_size=16,
                            color=GREY_A).next_to(ax.ax.c2p(3.65, 0), DOWN, buff=0.12))
        key = VGroup(label(r"teal: \ the Fed's staff \ (Greenbook)", font_size=16, color=CB),
                     label(r"gold: \ professional forecasters \ (SPF)", font_size=16, color=PRICE),
                     label(r"inflation over the next four quarters, \\ root mean squared error", font_size=15,
                           color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(ax, RIGHT, buff=0.4)
        tag = published_tag(r"Romer and Romer, \ \emph{AER} 90(3) (2000); \ Philadelphia Fed: \ Tealbook data set "
                            r"and SPF; \ GDP price index via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "And a claim about the staff's forecasts. Called it? <bookmark mark='a'/> In 2000, Christina and David "
            "Romer showed that the Federal Reserve's own staff forecast inflation better than commercial "
            "forecasters: once you knew the Greenbook, the others told you almost nothing. That is why, they "
            "argued, markets learn from the Fed's moves. <bookmark mark='b'/> The Greenbooks are released after "
            "five years, so the claim can be checked out of sample. Over the four quarters ahead, from 1969 to "
            f"1991, the staff's typical error was {K['rr']['rmse_gb']:.2f} points against the professional "
            f"forecasters' {K['rr']['rmse_spf']:.2f}. <bookmark mark='c'/> From 1992 to 2020 it was "
            f"{K['after']['rmse_gb']:.2f} against {K['after']['rmse_spf']:.2f}: the edge had gone, perhaps because "
            "the Fed began to say so much more. <bookmark mark='d'/> Partly right: true when they wrote it, of "
            "the years they studied, and not since."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag), FadeIn(ax), FadeIn(key))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], DOWN), FadeIn(labs[:2]), FadeIn(eras[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[2], DOWN), GrowFromEdge(bars[3], DOWN), FadeIn(labs[2:]), FadeIn(eras[1]),
                      Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("d")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
