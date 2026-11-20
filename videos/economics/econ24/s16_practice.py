from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ labour-market desks, \ job platforms", r"Who watches these flows, \ and who "
             r"is building the matching function?", "Chapter fourteen. In practice: labour-market desks and job "
             "platforms.", lit={2017: r"Horton", 2019: r"Belot, Kircher, Muller"}, scale=("firm", "nation"),
             horizon=("a month",))
        self.desk()
        self.platforms()
        self.who()

    def desk(self):
        j = load("jolts")
        b = load("beveridge")
        dash = VGroup(
            VGroup(label(r"unemployment", font_size=20, color=WORKER),
                   label(rf"{b['last_u']:.1f}\%", font_size=34, color=WORKER)),
            VGroup(label(r"openings per searcher", font_size=20, color=TIGHT),
                   label(rf"{b['last_v'] / b['last_u']:.2f}", font_size=34, color=TIGHT)),
            VGroup(label(r"quits a month", font_size=20, color=SEP),
                   label(rf"{j['quits'][-1] / 1000:.1f}m", font_size=34, color=SEP)),
            VGroup(label(r"hires a month", font_size=20, color=MATCH),
                   label(rf"{j['hires'][-1] / 1000:.1f}m", font_size=34, color=MATCH)),
        )
        for g in dash:
            g.arrange(DOWN, buff=0.2)
            box = RoundedRectangle(width=3.0, height=1.5, corner_radius=0.12, stroke_color=g[0].get_color(),
                                   stroke_width=2)
            box.move_to(g)
            g.add(box)
        dash.arrange(RIGHT, buff=0.3).move_to(UP * 1.7)
        when = label(rf"the latest JOLTS month, \ {b['last'][:7]}", font_size=18, color=GREY_B).next_to(dash, UP,
                                                                                                      buff=0.25)
        rows = VGroup(
            label(r"the central bank's labour desk reads the flows, \ not only the rate", font_size=23,
                  color=E.ACCENT),
            label(r"quits: \ workers leave when they are confident of finding better \ (the job ladder at work)",
                  font_size=21, color=SEP),
            label(r"openings per searcher: \ the model's $\theta$, \ watched as a gauge of wage pressure",
                  font_size=21, color=TIGHT),
            label(r"the natural rate: \ estimated, \ revised, \ argued over \ (Part 28)", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(dash, DOWN, buff=0.55)
        tag = data_tag(r"BLS, \ JOLTS and the CPS, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Who uses this? Start at a central bank. America's Federal Reserve is charged with maximum "
            "employment, and its staff watch the labour market the way this part has: as flows. "
            "<bookmark mark='a'/> Here is the latest month's dashboard: unemployment, openings per unemployed "
            "worker, quits, and hires. <bookmark mark='b'/> Quits matter because workers leave a job when they are "
            "confident of finding a better one: they are the job ladder in motion, and economists watch them as a "
            "signal of wage growth to come. <bookmark mark='c'/> Openings per searcher is the model's tightness, and in 2022 officials "
            "watched it closely as a gauge of how much pressure the labour market was putting on wages and prices. "
            "<bookmark mark='d'/> And the natural rate is estimated, revised and argued over, as Part twenty-eight "
            "will show."
        ) as vo:
            self.play(FadeIn(when), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in dash], lag_ratio=0.3), run_time=2)
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def platforms(self):
        rows = VGroup(
            label(r"job platforms are matching functions with an engineering team", font_size=25, color=E.ACCENT),
            label(r"Horton, \ 2017: \ an online labour market recommended workers to a random half of employers",
                  font_size=22, color=GREY_A),
            label(r"those openings were filled about 20\% more often, \ mostly technical jobs with few applicants, \ "
                  r"with no sign of crowding out", font_size=22, color=MATCH),
            label(r"Belot, \ Kircher and Muller, \ 2019: \ suggesting other occupations to job seekers in Scotland",
                  font_size=22, color=GREY_A),
            label(r"broader searches and more interviews, \ above all for those who had searched narrowly",
                  font_size=22, color=WORKER),
            label(r"the matching efficiency $A$ is not a constant of nature: \ it can be engineered", font_size=24,
                  color=TIGHT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Horton, JOLE 35(2) (2017): \ 345--385; \ Belot, Kircher and Muller, RES 86(4) (2019): "
                            r"\ 1411--1447", corner=DR, font_size=12)
        with self.voiceover(
            "The second place is a job platform. <bookmark mark='a'/> A job board is a matching function with an "
            "engineering team. <bookmark mark='b'/> John Horton ran an experiment on oDesk, an online labour market: "
            "for a random half of new openings, an algorithm recommended workers to the employer. "
            "<bookmark mark='c'/> Those openings were filled about twenty percent more often, mostly technical "
            "jobs that would otherwise have drawn few applicants, with no sign that the recommended workers crowded "
            "out others. <bookmark mark='d'/> Michèle Belot, Philipp Kircher and Paul Muller gave job seekers in "
            "Scotland a search tool that suggested other occupations that people like them had moved into. "
            "<bookmark mark='e'/> They searched more broadly and got more interviews, above all those who had been "
            "searching narrowly. <bookmark mark='f'/> In the model's terms, both raised A, the efficiency of "
            "matching. It is not a constant of nature. It can be engineered."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def who(self):
        cards = point_cards([
            (r"central banks", r"flows, \ tightness, \\ the natural rate", TIGHT),
            (r"employment services", r"benefits, \ job centres, \\ training", BENEFIT),
            (r"platforms", r"ranking, \ recommending, \\ pricing labour", MATCH),
            (r"employers and HR", r"vacancy costs, \\ retention, \ pay ladders", JOB),
        ], width=12.0, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"who uses this", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "So: central banks read the flows and tightness; treasuries and employment services design benefits "
            "and help people search; platforms rank and recommend; and employers price the cost of an empty "
            "desk against the cost of a raise."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards.cards], lag_ratio=0.5),
                      run_time=4)
        self.wait(1.0)
        self.clear_scene()
