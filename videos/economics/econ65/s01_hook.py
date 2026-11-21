from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403

NAMES = {"GBR": "Britain", "USA": "United States", "FRA": "France", "NLD": "Netherlands", "SWE": "Sweden",
         "DEU": "Germany", "JPN": "Japan", "KOR": "South Korea"}


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.scorecard()
        self.question()
        self.title()
        self.objectives()

    def story(self):
        cards = VGroup(
            history_card(r"1930", r"Keynes writes to his grandchildren", r"in the first year of the Depression, \ an "
                         r"essay: \ \emph{Economic Possibilities for our Grandchildren}", color=E.ACCENT, width=11.2,
                         font_size=21),
            history_card(r"forecast one", r"four to eight times richer", r"in a hundred years, \ the standard of life "
                         r"in progressive countries will be four to eight times as high", color=GAIN, width=11.2,
                         font_size=21),
            history_card(r"forecast two", r"a fifteen-hour week", r"three-hour shifts, \ the economic problem solved, "
                         r"\ and the real problem: \ how to use the freedom", color=WORK, width=11.2, font_size=21),
            history_card(r"on the way", r"technological unemployment", r"our discovery of means of economising the use "
                         r"of labour outrunning the pace at which we can find new uses for labour", color=MACH,
                         width=11.2, font_size=21),
        ).arrange(DOWN, buff=0.28).move_to(UP * 0.1)
        tag = published_tag(r"Keynes, \ \emph{Economic Possibilities for our Grandchildren}, \ The Nation and "
                            r"Athenaeum (1930)", corner=DL, font_size=12)
        with self.voiceover(
            "In 1930, in the first year of the Great Depression, John Maynard Keynes wrote an essay for his "
            "grandchildren. We are suffering just now, he wrote, from a bad attack of economic pessimism. He "
            "looked a hundred years ahead instead. <bookmark mark='a'/> In a hundred years, he wrote, the standard "
            "of life in the progressive countries will be between four and eight times as high as it is today. "
            "<bookmark mark='b'/> And people will work perhaps fifteen hours a week, in three-hour shifts, because the "
            "economic problem will be close to solved. The real problem will be how to use the freedom. <bookmark "
            "mark='c'/> On the way, he warned of a new disease, technological unemployment: unemployment due to "
            "our discovery of ways to economise on labour, outrunning the pace at which we find new uses for "
            "labour. The hundred years are up in 2030."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.1), FadeIn(tag))
            for mk, c in zip("abc", cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def scorecard(self):
        K = load("keynes")
        ratio = sorted(K["ratio"].items(), key=lambda kv: kv[1])
        axl = plane([-0.6, len(ratio) - 0.4], [0, 9], center=LEFT * 3.5 + DOWN * 0.5, x_length=5.6, y_length=4.4,
                    xticks=[], yticks=[0, 2, 4, 6, 8], ylabel=r"GDP per head, \ 2022 against 1930",
                    yfmt=lambda v: rf"{v:.0f}\times", font_size=14)
        bl = bars(axl, range(len(ratio)), [v for _, v in ratio], [GAIN] * len(ratio), width=0.62)
        band_ = shade(axl, [(-0.6, len(ratio) - 0.4)], 4, 8, GAIN, 0.12)
        names = VGroup(*[label(NAMES[c], font_size=13, color=GREY_A).rotate(PI / 6).next_to(
            axl.ax.c2p(k, 0), DOWN, buff=0.25) for k, (c, _) in enumerate(ratio)])
        vals = VGroup(*[label(f"{v:.1f}", font_size=14, color=GAIN).next_to(b, UP, buff=0.06)
                        for b, (_, v) in zip(bl, ratio)])
        kn = label(r"Keynes: \ 4 to 8 times", font_size=16, color=GAIN).move_to(axl.ax.c2p(1.0, 8.6))
        H = K["hours"]
        order = sorted(H, key=lambda c: H[c]["last"])
        axr = plane([-0.6, len(order) - 0.4], [0, 2600], center=RIGHT * 3.3 + DOWN * 0.5, x_length=5.6,
                    y_length=4.4, xticks=[], yticks=[0, 500, 1000, 1500, 2000, 2500],
                    ylabel=r"hours worked a year, \ per worker", yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"),
                    font_size=14)
        first = bars(axr, [k - 0.17 for k in range(len(order))], [H[c]["first"] for c in order],
                     [GREY_C] * len(order), width=0.32)
        last = bars(axr, [k + 0.17 for k in range(len(order))], [H[c]["last"] for c in order],
                    [WORK] * len(order), width=0.32)
        names_r = VGroup(*[label(NAMES[c], font_size=13, color=GREY_A).rotate(PI / 6).next_to(
            axr.ax.c2p(k, 0), DOWN, buff=0.25) for k, c in enumerate(order)])
        kline = seg(axr, -0.6, K["keynes_hours"], len(order) - 0.4, K["keynes_hours"], E.ACCENT, 2.4, dashed=True)
        klab = label(rf"Keynes: \ 15 hours a week $\approx$ {K['keynes_hours']} a year", font_size=15,
                     color=E.ACCENT).next_to(axr.ax.c2p(2.5, K["keynes_hours"]), DOWN, buff=0.12)
        key = legend_rows([(GREY_C, f"{H['USA']['first_year']}"), (WORK, f"{H['USA']['last_year']}")],
                          font_size=14).next_to(axr.ax.c2p(len(order) - 0.4, 2600), DL, buff=0.1)
        tag = data_tag(r"Maddison Project Database 2023; \ Penn World Table 11.0 (avh)", corner=DL, font_size=12)
        lo, hi = K["ratio_min"], K["ratio_max"]
        low = H[K["lowest"]]
        with self.voiceover(
            "How did he do? <bookmark mark='a'/> On the first forecast, very well. In six of the countries he would "
            f"have called progressive, GDP per head in 2022 was between {lo:.1f} and {hi:.1f} times its level of "
            "1930. Inside his range, and with eight years to spare. <bookmark mark='b'/> On the second, not at all. "
            "Fifteen hours a week is about seven hundred and eighty hours a year. <bookmark mark='c'/> Hours did "
            f"fall: in {NAMES[K['lowest']]} from about {low['first']:,.0f} a year in {low['first_year']} to "
            f"{low['last']:,.0f}. But nowhere is close to Keynes's line, and in the United States hours have hardly "
            "moved since the nineteen-eighties. We took most of our riches as more things, not more time."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(axl), FadeIn(band_), FadeIn(names), FadeIn(tag))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bl], lag_ratio=0.15), FadeIn(vals), FadeIn(kn),
                      run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(axr), FadeIn(names_r), Create(kline), FadeIn(klab))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in first], lag_ratio=0.1), run_time=1.2)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in last], lag_ratio=0.1), FadeIn(key), run_time=1.2)
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"which tasks do machines take, \ and which new ones appear?", font_size=26, color=MACH),
            label(r"why do general-purpose technologies take decades to pay?", font_size=26, color=GDP),
            label(r"what do the experiments with AI assistants find, \ and for whom?", font_size=26, color=TEXT),
            label(r"how do task-level gains add up, \ and what happens to wages?", font_size=26, color=WORK),
            label(r"can automating research make growth explode?", font_size=26, color=IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "Now the machines are learning to do more than the economising Keynes imagined. The question of this "
            "part: what happens to work, growth and incomes if machines can do most tasks? <bookmark mark='a'/> "
            "Which tasks do machines take, and which new ones appear? <bookmark mark='b'/> Why do general-purpose "
            "technologies take decades to show up in productivity? <bookmark mark='c'/> What do the experiments "
            "with AI assistants find, and for whom? <bookmark mark='d'/> How do task-level gains add up, and what "
            "happens to wages? <bookmark mark='e'/> And could automating research itself make growth explode?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        dots_ = VGroup(*[Circle(radius=0.16, stroke_color=WORK if k % 3 else MACH, stroke_width=2,
                                fill_color=WORK if k % 3 else MACH, fill_opacity=0.35) for k in range(12)])
        dots_.arrange(RIGHT, buff=0.18)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 65 \ $\cdot$ \ The Economics of AI", font_size=34, color=E.ACCENT)
        VGroup(dots_, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part sixty-five: the economics of AI."):
            self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dots_], lag_ratio=0.08), run_time=1.4)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XII \ $\cdot$ \ The Frontier", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"the task model: \ displacement, \ productivity and new tasks, \ with its wages and labour share",
            r"general-purpose technologies and the productivity J-curve",
            r"what the experiments find, \ and how task gains become aggregate ones",
            r"growth with automated research, \ Baumol's bottleneck, \ and Nordhaus's tests",
            r"market structure, \ agents that trade, \ and policy",
        ], color=E.ACCENT, font_size=28, width=13.0)
        with self.voiceover(
            "Part sixty-four was about machines that help economists. This part is about machines that change the "
            "economy. By the end you will know <bookmark mark='a'/> the task model, in which automation displaces "
            "workers, raises productivity, and is offset by new tasks, and what that does to wages and labour's "
            "share; <bookmark mark='b'/> why general-purpose technologies take decades to pay, and why measured "
            "productivity first falls; <bookmark mark='c'/> what the experiments with AI assistants find, and the "
            "arithmetic that turns task-level gains into an economy-wide number; <bookmark mark='d'/> what happens "
            "to growth when research itself is automated, why the tasks left to people set the pace, and how to "
            "test for an explosion in the data; <bookmark mark='e'/> and who captures the gains, what happens when "
            "software trades with software, and what policy can do."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
