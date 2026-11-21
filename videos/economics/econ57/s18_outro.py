from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403

PROBLEMS = [
    r"Diebold and Mariano: \ why does the test for forecasts $h$ quarters ahead need a standard error that allows "
    r"for $h - 1$ lags of autocorrelation?",
    r"Bates and Granger: \ derive the weight that minimizes the variance of $w e_1 + (1 - w) e_2$, \ and evaluate it "
    r"for errors of s.d. 0.99 and 1.02 with correlation 0.73.",
    r"Pseudo real time: \ why is a nowcast scored on today's revised data, \ with the release calendar imposed, \ "
    r"likely to look better than it was?",
    r"The Sahm rule on today's data fired in 2003; \ in real time it did not. \ Give two reasons the two can differ.",
    r"A minister asks: \ `will there be a recession next year?' \ Write the three-sentence answer this part's Dial "
    r"allows.",
    r"$\bigstar$ \ Hamilton: \ with expansions that persist with probability 0.95 a quarter and recessions with "
    r"0.75, \ find the share of time in recession and the average length of each regime.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).move_to(UP * 2.4)
        a = wrapped_label(r"Right now: \ fairly well, \ and better each week, \ once the data are read as they arrive "
                          r"and revised. \ Next year: \ hardly better than the average of the past, \ and recessions "
                          r"almost never, \ because the best guess of a rare and randomly timed event is never the "
                          r"event. \ So read the present carefully, \ say how uncertain the future is, \ and keep "
                          r"score.", 11.6, 26, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([F["t"][0], F["t"][-1]], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["p"])
        v = (v - np.nanmin(v)) / (np.nanmax(v) - np.nanmin(v))
        logo = path(mini, F["t"], v, NOW, 2.0, smooth=False).next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: what is the economy doing right now, and how good is anyone's guess about next year? <bookmark "
            "mark='a'/> Right now, fairly well, and better each week, if the data are read as they arrive and "
            "their revisions expected. Next year, hardly better than the average of the past, and recessions "
            "almost never, because the best guess of a rare and randomly timed event is never the event. So read "
            "the present carefully, say how uncertain the future is, and keep score."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=10.0, rate_func=linear)
        self.clear_scene()

    def recap(self):
        R, S_, I_, B, P, SC, G, Rg = (load(x) for x in ("revisions", "seasonal", "island", "bridge", "probit",
                                                         "score", "greenbook", "regimes"))
        r0 = SC["rows"]
        items = [
            (r"recessions are recognized, \ not forecast: \ 5 of 153 a year ahead", NOW),
            (rf"GDP's first estimate moves by {R['mae']:.1f} points on average; \ 2008Q4 doubled", FIRST),
            (r"seasonal adjustment removes a pattern, \ and can invent one", LATEST),
            (r"Play it: \ the survey said `fall' before the hard data did", NOW),
            (rf"nowcast errors fall as the data arrive: \ {I_['rmse'][0]:.1f} to {I_['rmse'][-1]:.1f}", SPF),
            (rf"the yield curve: \ AUC {P['auc']:.2f}, \ and a 25-month false alarm", GB),
            (r"the Sahm rule: \ fast recognition, \ two false signals", ERR),
            (rf"forecasts beat the average for two quarters, \ then match it \ ({r0[-1]['rmse']:.1f})", SPF),
            (r"the Fed's staff forecast inflation better than the market", GB),
            (r"the best forecast a year ahead is never a recession", ERR),
            (r"new data and text: \ faster, \ to be checked against the slow numbers", LATEST),
            (r"say the number, \ the range, \ and what would change your mind", E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 57, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del S_, B, G, Rg
        with self.voiceover(
            "Part fifty-seven in twelve lines. <bookmark mark='r1'/> Recessions are recognized, not forecast. "
            "<bookmark mark='r2'/> A first estimate of GDP is a guess, revised by about a point and a half. "
            "<bookmark mark='r3'/> Seasonal adjustment removes a pattern, and can invent one. <bookmark mark='r4'/> "
            "In the Play it, the survey said 'fall' before the hard data did. <bookmark mark='r5'/> Nowcast errors "
            "fall as the data arrive. <bookmark mark='r6'/> The yield curve has a good record, and a long false "
            "alarm. <bookmark mark='r7'/> The Sahm rule recognizes recessions fast, and has cried wolf twice. "
            "<bookmark mark='r8'/> Professional forecasts beat the average for about two quarters, then match it. "
            "<bookmark mark='r9'/> The Federal Reserve's staff forecast inflation better than the market. "
            "<bookmark mark='r10'/> The best forecast a year ahead is never a recession. <bookmark mark='r11'/> New "
            "data and text are faster, and must be checked against the slow numbers. <bookmark mark='r12'/> And "
            "say the number, the range, and what would change your mind."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems: why overlapping forecasts need a careful standard error; Bates and Granger's weight; why "
            "pseudo real time flatters a nowcast; why the Sahm rule differs between today's data and real time; "
            "the three sentences a minister should hear; and a starred problem on Hamilton's regimes. Full "
            "solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Graham Elliott and Allan Timmermann, \emph{Economic Forecasting} (2016)",
             r"Marta Ba\'nbura, \ Domenico Giannone, \ Michele Modugno and Lucrezia Reichlin, \ `Now-casting and the "
             r"real-time data flow', \emph{Handbook of Economic Forecasting} 2A (2013)",
             r"Dean Croushore, \ `Frontiers of real-time data analysis', \emph{JEL} 49(1) (2011)"],
            [r"Bates and Granger (1969); \ Mankiw and Shapiro (1986); \ Hamilton (1989); \ Diebold and Mariano "
             r"(1995)",
             r"Estrella and Mishkin (1998); \ Romer and Romer (2000); \ Stock and Watson (2002, 2004)",
             r"Giannone, \ Reichlin and Small (2008); \ Henderson, \ Storeygard and Weil (2012); \ Baker, \ Bloom and "
             r"Davis (2016)",
             r"Cavallo and Rigobon (2016); \ An, \ Jalles and Loungani (2018); \ Hansen, \ McMahon and Prat (2018); "
             r"\ Sahm (2019)",
             r"Gentzkow, \ Kelly and Taddy (2019); \ Blanchet, \ Saez and Zucman (2022); \ Bernanke (2024); \ "
             r"Chetty et al.\ (2024)"])
        with self.voiceover(
            "The reading: Graham Elliott and Allan Timmermann's book on economic forecasting; the handbook chapter "
            "on nowcasting by Marta Bańbura and her coauthors; and Dean Croushore on real-time data. Then the "
            "papers, from Bates and Granger to the Bernanke review."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1936, r"the Flood Control Act", r"projects worth building `if the benefits to whomsoever "
                          r"they may accrue are in excess of the estimated costs'", color=E.ACCENT, width=10.4,
                          font_size=23)
        nxt = VGroup(label(r"Next: \ Part 58 \ $\cdot$ \ Act XI, \ Economics at Work", font_size=30, color=GREY_B),
                     label(r"Scoring the Bill", font_size=46),
                     label(r"is this project, \ or this law, \ worth it?", font_size=24, color=E.ACCENT)).arrange(
            DOWN, buff=0.22)
        head = label(r"from reading the economy to pricing a policy", font_size=26, color=GREY_A).to_edge(UP,
                                                                                                         buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"discounting", SPF), (r"valuing a life", ERR), (r"budget scoring", GB),
                                         (r"microsimulation", LATEST))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, from reading the economy to pricing a policy. <bookmark mark='a'/> In 1936 Congress told "
            "the Army's engineers to build flood works only if the benefits, to whomsoever they may accrue, "
            "exceeded the costs. <bookmark mark='b'/> Discounting the future, valuing a statistical life, scoring "
            "a bill's cost, and simulating who gains. <bookmark mark='c'/> Part fifty-eight: scoring the bill."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
