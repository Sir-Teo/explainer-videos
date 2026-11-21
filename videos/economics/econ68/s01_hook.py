from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.paris()
        self.city()
        self.question()
        self.title()
        self.objectives()

    def paris(self):
        B = tables.BASTIAT_1845.data
        hc = history_card(r"1845", r"who feeds Paris?", r"Fr\'ed\'eric Bastiat, \ \emph{Economic Sophisms}: \ a "
                          r"million people, \ fed every day, \ and nobody planning it", color=E.ACCENT, width=11.6,
                          font_size=22).to_edge(UP, buff=0.5)
        q = VGroup(
            label(r"`How does each succeeding day manage to bring to this gigantic market \\ just what is "
                  r"necessary, \ neither too much nor too little?'", font_size=24, color=WHITE),
            label(r"Part 1 answered with prices; \ sixty-six parts since asked what else is needed", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.5).next_to(hc, DOWN, buff=0.7)
        tag = published_tag(r"Bastiat, \ \emph{Economic Sophisms} (1845), \ ch.\ 18; \ Goddard's translation",
                            corner=DL, font_size=12)
        with self.voiceover(
            "This series began in a city. <bookmark mark='a'/> In 1845 Frédéric Bastiat looked at Paris, a "
            "million people who would all go hungry within days if supplies stopped, and wondered why they slept "
            f"peacefully. <bookmark mark='b'/> {B['how']} <bookmark mark='c'/> Part one's answer was prices. "
            "Sixty-six parts since have asked what else it takes: institutions, money, banks, states, and the "
            "evidence to tell which claims are true."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(q[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(q[1]))
        self.clear_scene()

    def city(self):
        O = load("official")
        En = load("entries")
        hc = history_card(r"5 January 2025", r"a price on a street", r"New York begins charging \$9 to drive into "
                          r"Manhattan below 60th Street from 5 am to 9 pm on weekdays, \ \$2.25 at night", color=TOLL,
                          width=11.6, font_size=22).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the first charge for entering a downtown in the United States", font_size=22, color=GREY_A),
            label(rf"about {En['weekday_all'] / 1000:.0f},000 vehicles still enter on an average weekday",
                  font_size=22, color=DATA),
            label(rf"the state: \ {O['fewer_share'] * 100:.0f}\% fewer vehicles in the first year, \ "
                  rf"\${O['revenue_m']} million for transit", font_size=22, color=BUS),
            label(r"the question of this part: \ what did it do, \ and how would an economist find out?",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(hc, DOWN, buff=0.6)
        tag = published_tag(r"MTA; \ Office of the Governor of New York (5 January 2026); \ MTA open data", corner=DL,
                            font_size=12)
        with self.voiceover(
            "This part ends in a city too. <bookmark mark='a'/> On the fifth of January 2025, New York began charging "
            "nine dollars to drive into Manhattan below 60th Street in the day, two dollars twenty-five at night: "
            "the first price on entering a downtown in the United States, and William Vickrey's idea of Part "
            "fifteen, put into law. <bookmark mark='b'/> On an average weekday about "
            f"{En['weekday_all'] / 1000:.0f} thousand vehicles still enter. <bookmark mark='c'/> A year in, the state "
            f"said {O['fewer_share'] * 100:.0f} percent fewer vehicles were entering, and {O['revenue_m']} million "
            "dollars had been raised for transit. <bookmark mark='d'/> Is that right? What did the charge do, to "
            "traffic, to buses, to when people travel? This last part carries one question from an idea to a "
            "paper, with everything the series has built."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 36, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"a question: \ important, \ answerable, \ not yet answered", font_size=26, color=FIRST),
            label(r"data, \ described before anything is estimated", font_size=26, color=DATA),
            label(r"a design, \ with its threats listed in advance", font_size=26, color=TRUE),
            label(r"a model, \ the smallest that speaks to the estimates, \ and a counterfactual", font_size=26,
                  color=MODEL),
            label(r"and the series' accounts, \ closed", font_size=26, color=TOLL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question of the part: how is a new piece of economics made? <bookmark mark='a'/> It starts with a "
            "question that matters, can be answered, and has not been. <bookmark mark='b'/> Then the data, "
            "described before anything is estimated. <bookmark mark='c'/> A design, with its threats written down "
            "before the results are seen. <bookmark mark='d'/> A model, the smallest that speaks to the estimates, "
            "and a counterfactual: a policy that was not tried. <bookmark mark='e'/> And, because this is the last "
            "part, the series' accounts, closed."
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 68 \ $\cdot$ \ The Dissertation", font_size=34, color=E.ACCENT)
        bar = VGroup(*[Rectangle(width=0.16, height=0.12 + 0.02 * k, stroke_width=0, fill_color=E.ACCENT,
                                 fill_opacity=0.25 + 0.01 * k) for k in range(68)]).arrange(RIGHT, buff=0.02,
                                                                                         aligned_edge=DOWN)
        VGroup(bar, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part sixty-eight: the dissertation."):
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bar], lag_ratio=0.02), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XII \ $\cdot$ \ The Frontier", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"how to choose a question, \ find the data and describe it first",
            r"how to design a study and list its threats before the results",
            r"what New York's charge did to traffic, \ buses and the clock, \ and what the design cannot say",
            r"how to build the smallest model and carry uncertainty into a counterfactual",
            r"what the series' Facts, \ Dials and Tableau finally show",
        ], color=E.ACCENT, font_size=28, width=13.0)
        with self.voiceover(
            "Part sixty-seven asked how much of economics is true. This part makes a piece of it. By the end you "
            "will know <bookmark mark='a'/> how to choose a question, find its data and describe them first; "
            "<bookmark mark='b'/> how to choose a design and list its threats before you see a result; <bookmark "
            "mark='c'/> what New York's charge did to traffic, to buses and to the clock, and what the design cannot "
            "say; <bookmark mark='d'/> how to build the smallest model that speaks to the estimates, and carry its "
            "uncertainty into a policy that was not tried; <bookmark mark='e'/> and what the series' Facts, Dials and "
            "Tableau finally show."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
