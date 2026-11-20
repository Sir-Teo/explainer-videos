from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.mailing()
        self.random()
        self.aggregate()
        self.question()
        self.advice()
        self.title()
        self.objectives()

    def mailing(self):
        r = load("rebate")
        weeks = VGroup()
        for d in r["digits"]:
            box = RoundedRectangle(width=1.08, height=1.25, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2)
            num = label(rf"week {d + 1}", font_size=15, color=GREY_B).next_to(box, UP, buff=0.08)
            dig = label(rf"\ldots\,{d}\,x", font_size=24, color=WHITE).move_to(box)
            weeks.add(VGroup(box, num, dig))
        weeks.arrange(RIGHT, buff=0.12).move_to(DOWN * 0.2)
        cheques = VGroup()
        for w in weeks:
            ch = VGroup(Rectangle(width=0.8, height=0.4, stroke_color=SAVE, stroke_width=2, fill_color=SAVE,
                                  fill_opacity=0.2), label(r"\$", font_size=20, color=SAVE))
            ch[1].move_to(ch[0])
            ch.move_to(w[0].get_center() + DOWN * 0.95)
            cheques.add(ch)
        head = label(r"the 2001 tax rebate: \ \$300 for a single filer, \ \$600 for a couple", font_size=26,
                     color=SAVE).to_edge(UP, buff=0.7)
        sub = label(r"the mailing week set by the second-to-last digit of the Social Security number", font_size=22,
                    color=GREY_A).next_to(head, DOWN, buff=0.3)
        ends = VGroup(label(r"late July", font_size=19, color=GREY_B).next_to(weeks, DOWN, buff=1.05).align_to(
            weeks, LEFT), label(r"late September", font_size=19, color=GREY_B).next_to(weeks, DOWN, buff=1.05).align_to(
            weeks, RIGHT))
        tag = published_tag(r"Johnson, Parker and Souleles, AER 96(5) (2006): \ 1589--1610", corner=DR, font_size=12)
        with self.voiceover(
            "In the summer of 2001 the United States Treasury began mailing tax rebate cheques: three hundred dollars "
            "to a single filer, six hundred to a couple, to about two-thirds of American households. "
            "<bookmark mark='a'/> There were too many to send at once. So they went out over ten weeks, from late "
            "July to late September, and the week in which a household's cheque was mailed was set by the "
            "second-to-last digit of its Social Security number. <bookmark mark='b'/> A zero went first, a nine "
            "went last."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(w) for w in weeks], lag_ratio=0.1),
                      FadeIn(ends), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(sub))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in cheques], lag_ratio=0.3), run_time=4)
        self.clear_scene()

    def random(self):
        rows = rows_card([
            (r"the digit has nothing to do with a household's income, \ needs or plans", GREY_A, 25),
            (r"so the timing was random: \ an experiment no one designed", SAVE, 27),
            (r"and every household knew in advance when its cheque would come", GREY_A, 25),
            (r"the theory of the day: \ money you know is coming is already in your spending", INCOME, 25),
            (r"so the day it arrives should change nothing", INCOME, 25),
        ])
        with self.voiceover(
            "That digit has nothing to do with a household's income, its needs or its plans. "
            "<bookmark mark='a'/> So the timing was random: an experiment that no one had designed. "
            "<bookmark mark='b'/> And the timing was announced. Every household could know when its cheque would "
            "come. <bookmark mark='c'/> The theory of the day, Milton Friedman's, says that money you know is "
            "coming is already in your spending plans. <bookmark mark='d'/> So the day it arrives should change "
            "nothing."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def aggregate(self):
        r = load("rebate")
        t = np.array(r["t"])
        jun = r["dates"].index("2001-06-01")
        Y = np.array(r["Y"]) / r["Y"][jun] * 100
        C = np.array(r["CNS"]) / r["CNS"][jun] * 100
        ax = plane([2000.5, 2002.5], [97, 104.5], center=LEFT * 1.4 + DOWN * 0.4, x_length=8.6, y_length=5.0,
                   xticks=[2001, 2002], yticks=[98, 100, 102, 104], ylabel=r"June 2001 $= 100$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", font_size=16)
        band = Rectangle(width=ax.ax.c2p(2001.75, 0)[0] - ax.ax.c2p(2001.5, 0)[0], height=5.0 * 7 / 7.5,
                         stroke_width=0, fill_color=SAVE, fill_opacity=0.12)
        band.move_to([(ax.ax.c2p(2001.5, 100)[0] + ax.ax.c2p(2001.75, 100)[0]) / 2, ax.ax.c2p(0, 100.75)[1], 0])
        yl = path(ax, t, Y, color=INCOME, width=4, smooth=False)
        cl = path(ax, t, C, color=SPEND, width=4, smooth=False)
        side = VGroup(
            label(r"real disposable income", font_size=20, color=INCOME),
            label(r"real spending on nondurables \\ and services", font_size=20, color=SPEND),
            label(rf"saving rate: \ {r['saving_june']:.1f}\% in June, \\ {r['saving_sept']:.1f}\% in September, \ "
                  rf"{r['saving_oct']:.1f}\% in October", font_size=19, color=SAVE),
            label(r"September also brought \\ the attacks of the eleventh", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(rf"BEA via FRED: \ DSPIC96, \ PCEND, \ PCES and their price indexes; \ retrieved "
                       rf"{data.fred('PCE')['retrieved']}", corner=DR, font_size=12)
        with self.voiceover(
            "Here is what the national accounts saw, month by month, with June 2001 set to one hundred. "
            "<bookmark mark='a'/> Disposable income, after tax and in real terms, jumps in July, August and "
            "September, as the cheques go out. <bookmark mark='b'/> Spending on nondurable goods and services "
            "barely moves. <bookmark mark='c'/> The saving rate rises from "
            f"{r['saving_june']:.1f} percent in June to {r['saving_sept']:.1f} percent in September, and falls back "
            "in October. So did households simply save their cheques? <bookmark mark='d'/> The aggregate cannot say. "
            "Too much else happened that autumn, the attacks of September the eleventh among it. But the random "
            "timing can. Three economists, David Johnson, Jonathan Parker and Nicholas Souleles, compared households "
            "whose cheques came early with households whose cheques came late. The day of arrival mattered. How "
            "much, you'll guess in a moment."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(band))
            vo.wait_until("a")
            self.play(Create(yl), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(cl), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how should a household that looks ahead spread its income over its life?", font_size=26,
                  color=INCOME),
            label(r"why do real households spend windfalls faster than that theory says?", font_size=26,
                  color=SPEND),
            label(r"and what does it mean for stimulus cheques, \ pensions and national saving?", font_size=26,
                  color=SAVE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: how do households decide how much to spend today? <bookmark mark='a'/> How "
            "should a household that looks ahead spread its income over its life? <bookmark mark='b'/> Why do real "
            "households spend windfalls faster than that theory says? <bookmark mark='c'/> And what does it mean "
            "for stimulus cheques, for pensions, and for how much a nation saves?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def advice(self):
        box = RoundedRectangle(width=10.6, height=3.0, corner_radius=0.15, stroke_color=GREY_B, stroke_width=2,
                               fill_color=GREY_E, fill_opacity=0.5)
        t = VGroup(label(r"Not financial advice", font_size=38, color=WHITE),
                   label(r"this part is about how saving is modelled and measured; \\ its households, pensions and "
                         r"windfalls are illustrations, \\ not recommendations for anyone's money", font_size=24,
                         color=GREY_A)).arrange(DOWN, buff=0.35).move_to(box)
        with self.voiceover(
            "One card before we start. This part is about how saving is modelled and measured. Its households, "
            "pensions and windfalls are illustrations, not advice about anyone's money."
        ):
            self.play(FadeIn(box), FadeIn(t))
        self.wait(1.0)
        self.clear_scene()

    def title(self):
        r = load("rebate")
        mini = plane([2000.5, 2002.5], [97, 104.5], x_length=4.2, y_length=1.5)
        jun = r["dates"].index("2001-06-01")
        logo = VGroup(path(mini, r["t"], np.array(r["Y"]) / r["Y"][jun] * 100, INCOME, width=4, smooth=False),
                      path(mini, r["t"], np.array(r["CNS"]) / r["CNS"][jun] * 100, SPEND, width=4, smooth=False))
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 22 \ $\cdot$ \ Consumption and Saving", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part twenty-two: consumption and saving."):
            self.play(Create(logo), run_time=1.4)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act V \ $\cdot$ \ The Long Run", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"Keynes's consumption function and Kuznets's puzzle; \ Friedman's answer",
            r"permanent income and the life cycle; \ Hall's random walk and its tests",
            r"precautionary saving solved on a grid; \ the rebate experiments; \ the wealthy hand-to-mouth",
            r"Ricardian equivalence; \ overlapping generations and pensions; \ China's saving",
            r"a dial on the propensity to spend; \ stimulus design; \ spending through unemployment",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Five. <bookmark mark='a'/> You'll meet Keynes's consumption function, the "
            "puzzle Simon Kuznets found in it, and Friedman's answer. <bookmark mark='b'/> You'll derive permanent "
            "income and the life cycle, and test Robert Hall's claim that consumption is a random walk on sixty "
            "years of American data. <bookmark mark='c'/> You'll solve a household's precautionary saving on a "
            "grid, read the rebate experiments, and meet households that are rich and still live hand to mouth. "
            "<bookmark mark='d'/> Then whether government debt is wealth, how generations trade with one another "
            "through pensions, and why China saves so much. <bookmark mark='e'/> And a dial on how much of a "
            "windfall people spend, the design of stimulus, and spending through unemployment."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
