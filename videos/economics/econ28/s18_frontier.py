from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ how people really form expectations", r"What do surveys say about the "
             r"expectations in the models?", "Chapter sixteen. Frontier: how people really form expectations.",
             lit={2018: r"Coibion, Gorodnichenko and Kumar", 2022: r"Weber and coauthors"},
             scale=("person", "firm"), horizon=("a year",))
        self.households()
        self.firms()
        self.open_()

    def households(self):
        X = load("expect")
        ax = plane([1978, 2027], [-3, 15], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[0, 5, 10, 15], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        act = path(ax, X["t"], X["actual"], color=INFL, width=2, smooth=False)
        mi = path(ax, X["t"], X["mich"], color=EXPECT, width=3, smooth=False)
        side = VGroup(
            label(r"gold: \ households' median expectation \\ for the next 12 months", font_size=19, color=EXPECT),
            label(r"red: \ inflation over the past 12", font_size=19, color=INFL),
            label(rf"2010s: \ households expected {X['mich_mean_2010s']:.1f}\%; \\ inflation averaged "
                  rf"{X['cpi_mean_2010s']:.1f}\%", font_size=19, color=HOLD),
            label(r"expectations track recent prices, \\ especially of petrol and groceries", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"University of Michigan Surveys of Consumers; \ BLS: \ CPI; \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "The models of this part make strong assumptions about expectations. Since the 2010s, economists have "
            "asked people directly. <bookmark mark='a'/> In gold, the median American household's expectation of "
            "inflation over the next twelve months, from the University of Michigan's survey, since 1978. "
            "<bookmark mark='b'/> In red, inflation over the previous twelve. The gold line follows the red one, "
            "with a lag: households extrapolate. <bookmark mark='c'/> Through the 2010s, households expected about "
            f"{X['mich_mean_2010s']:.0f} percent, while inflation averaged under two. <bookmark mark='d'/> Michael "
            "Weber and his coauthors show that households' expectations are high, widely dispersed, and driven by "
            "the prices they see most often, at the petrol station and the supermarket."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(mi), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(act), FadeIn(side[1]), run_time=1.5)
            for mk, r_ in zip("cd", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def firms(self):
        rows = VGroup(
            label(r"and firms?", font_size=28, color=E.ACCENT),
            label(r"Coibion, \ Gorodnichenko and Kumar, \ 2018: \ New Zealand's firm managers, \ in a country with "
                  r"an inflation target since 1990", font_size=21, color=CB),
            label(r"most could not say what the target was; \ their forecasts were far apart", font_size=22,
                  color=HOLD),
            label(r"in calm times, \ paying attention to inflation is not worth the trouble: \ rational "
                  r"inattention", font_size=22, color=EXPECT),
            label(r"so central bank announcements reach people slowly, \ unless inflation is high enough to notice",
                  font_size=22, color=INFL),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Coibion, \ Gorodnichenko and Kumar, \ AER 108(9) (2018); \ Weber, \ D'Acunto, \ "
                            r"Gorodnichenko and Coibion, \ JEP 36(3) (2022)", corner=DR, font_size=12)
        with self.voiceover(
            "And firms? <bookmark mark='a'/> Olivier Coibion, Yuriy Gorodnichenko and Saten Kumar surveyed firm "
            "managers in New Zealand, the first country to adopt an inflation target. <bookmark mark='b'/> Most "
            "could not say what the target was, and their forecasts of inflation were far apart. "
            "<bookmark mark='c'/> In calm times, keeping track of inflation is not worth the trouble; economists "
            "call it rational inattention. <bookmark mark='d'/> So what central banks announce reaches people "
            "slowly, unless inflation is high enough to notice, which is when it matters most."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def open_(self):
        rows = VGroup(
            label(r"open questions", font_size=30, color=E.ACCENT),
            label(r"if expectations are not rational, \ which model of them should policy use?", font_size=23,
                  color=EXPECT),
            label(r"could a central bank steer expectations by speaking to households directly?", font_size=23,
                  color=CB),
            label(r"is the Phillips curve flat, \ hidden, \ or bent? \ and is the 2\% anchor safe after 2021?",
                  font_size=23, color=INFL),
            label(r"what is the natural rate now, \ and how would we know?", font_size=23, color=OUTPUT),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.1)
        with self.voiceover(
            "The questions still open. <bookmark mark='a'/> If expectations are not rational, which model of them "
            "should policy use? <bookmark mark='b'/> Could a central bank steer expectations by speaking to "
            "households in plain words? <bookmark mark='c'/> Is the Phillips curve flat, hidden or bent, and is the "
            "two percent anchor as safe after 2021 as it was before? <bookmark mark='d'/> And what is the natural "
            "rate of unemployment now, and how would anyone know?"
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
