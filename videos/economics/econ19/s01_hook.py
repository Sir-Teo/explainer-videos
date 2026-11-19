from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.malthus()
        self.turn()
        self.question()
        self.title()
        self.objectives()

    def malthus(self):
        t = tables.MALTHUS_1798.data
        hc = history_card(1798, r"the Reverend Thomas Malthus, \ a country curate", r"\emph{An Essay on the Principle "
                          r"of Population}, \ published anonymously", color=POP, width=11.0,
                          font_size=24).to_edge(UP, buff=0.4)
        qc = quote_card(tex_safe(t["ratios"]), r"Malthus (1798), \ chapter 1", width=10.6, font_size=27,
                        color=POP).next_to(hc, DOWN, buff=0.5)
        rows = VGroup(
            label(r"people multiply: \ 1, \ 2, \ 4, \ 8, \ 16 \ldots \quad food grows: \ 1, \ 2, \ 3, \ 4, \ 5 \ldots",
                  font_size=24, color=GREY_A),
            label(r"so whenever living standards rise, \ more children survive, \ until they fall back", font_size=25,
                  color=WAGE),
        ).arrange(DOWN, buff=0.35).next_to(qc, DOWN, buff=0.5)
        tag = published_tag(tables.MALTHUS_1798.tag, corner=DR, font_size=13)
        with self.voiceover(
            "In 1798 a country curate, the Reverend Thomas Malthus, published an essay, without his name on it, on the "
            "principle of population. <bookmark mark='a'/> Its argument fits in two sentences. Population, when "
            "unchecked, increases in a geometrical ratio. Subsistence increases only in an arithmetical ratio. "
            "<bookmark mark='b'/> People multiply, one, two, four, eight, while food grows, one, two, three, four. "
            "<bookmark mark='c'/> So whenever living standards rise, more children survive and more people marry, "
            "until there are enough mouths to push living standards back down. Misery and vice, in his words, keep "
            "the numbers in check."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(qc, shift=UP * 0.1))
            for mk, r in zip("bc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def turn(self):
        p = load("playit")
        years, wage = np.array(p["years"], float), np.array(p["wage"])
        ax = plane([1260, 2020], [0, 650], center=DOWN * 0.3, x_length=11.6, y_length=5.2,
                   xticks=[1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000], yticks=[0, 100, 200, 300, 400, 500, 600],
                   ylabel=r"English real wages, \ 1900 = 100", xfmt=lambda v: f"{v:.0f}", font_size=18)
        k = int(np.searchsorted(years, 1798))
        before = path(ax, years[:k + 1], wage[:k + 1], color=WAGE, width=3, smooth=False)
        after = path(ax, years[k:], wage[k:], color=GDP, width=4, smooth=False)
        mark = VGroup(DashedLine(ax.ax.c2p(1798, 0), ax.ax.c2p(1798, 560), color=POP, stroke_width=2),
                      label(r"1798", font_size=20, color=POP).next_to(ax.ax.c2p(1798, 560), UP, buff=0.08))
        n1 = label(r"five centuries of Malthus: \ wages rise and fall, \ but go nowhere", font_size=21,
                   color=WAGE).move_to(ax.ax.c2p(1500, 200))
        n2 = label(rf"then a climb that has not stopped: \ $\times${p['key']['2016']['wage'] / p['key']['1800']['wage']:.0f}"
                   rf" \ by 2016", font_size=21, color=GDP).move_to(ax.ax.c2p(1600, 470))
        src = data_tag(data.cite("millennium"), corner=DR,
                       font_size=12)
        with self.voiceover(
            "As a description of every century before his, the theory was good. <bookmark mark='a'/> Here are the "
            "real wages of English workers from the thirteenth century to his. They rise and fall, sometimes a long "
            "way, but over five hundred years they go nowhere. <bookmark mark='b'/> And here is what happened next. "
            f"By 2016 real wages were about {p['key']['2016']['wage'] / p['key']['1800']['wage']:.0f} times their "
            "level of 1800. <bookmark mark='c'/> Malthus published in the one country, and in the one generation, "
            "in which his theory had just stopped being true."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(before), run_time=4, rate_func=linear)
            self.play(FadeIn(n1), Create(mark[0]), FadeIn(mark[1]))
            vo.wait_until("b")
            self.play(Create(after), run_time=3, rate_func=linear)
            self.play(FadeIn(n2))
            vo.wait_until("c")
            self.play(Indicate(mark[1], color=WHITE, scale_factor=1.3))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what kept almost everyone near subsistence for millennia?", font_size=29, color=WAGE),
            label(r"why did the escape begin in north-western Europe, \ around 1800?", font_size=29, color=GDP),
            label(r"and why did people, \ once richer, \ choose to have fewer children?", font_size=29, color=POP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Act Five is about the long run, and it begins with the oldest question in economics. Why was almost "
            "everyone poor for almost all of history, and what changed? <bookmark mark='a'/> What kept nearly "
            "everyone near subsistence for thousands of years? <bookmark mark='b'/> Why did the escape begin in "
            "north-western Europe, around 1800, and not somewhere else, or earlier? <bookmark mark='c'/> And why, "
            "once they were richer, did people choose to have fewer children, the opposite of what Malthus expected?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        p = load("playit")
        years, g = np.array(p["years"], float), np.array(p["gdppc"])
        mini = plane([1270, 2016], [0, 30000], x_length=4.2, y_length=1.6)
        logo = VGroup(path(mini, years, g, color=GDP, width=4, smooth=False))
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 19 \ $\cdot$ \ The Great Escape", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part nineteen: the great escape."):
            self.play(Create(logo), run_time=1.4)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act V \ $\cdot$ \ The Long Run", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"when the climb began; \ the Malthusian model, \ derived and run",
            r"Malthus tested on seven centuries of English wages; \ the Black Death as an experiment",
            r"why Britain, \ why 1760, \ why not China; \ the great divergence",
            r"the Industrial Revolution in numbers; \ the demographic transition; \ one model for it all",
            r"was it good? \ a dial on growth before the escape; \ forecasts; \ deep roots",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part opens Act Five, the long run. <bookmark mark='a'/> You'll find when the climb began, then "
            "derive the Malthusian model and run it. <bookmark mark='b'/> You'll test it on seven centuries of "
            "English wages, and watch the Black Death run Malthus's mechanism backwards. <bookmark mark='c'/> Then "
            "the arguments over why Britain, why the 1760s, and why not China, and a data film of the great "
            "divergence. <bookmark mark='d'/> The Industrial Revolution in numbers, the demographic transition, and "
            "one model for the whole story. <bookmark mark='e'/> And whether it was good, a dial on growth before "
            "the escape, a famous failed forecast, and the frontier of deep roots."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
