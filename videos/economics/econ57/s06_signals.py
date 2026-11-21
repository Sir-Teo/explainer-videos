from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403


def _t(k: str) -> float:
    return int(k[:4]) + (int(k[5:7]) - 1) / 12


class Signals(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The yield curve and the Sahm rule", r"Which signals warn of a recession, \ and how often do "
             r"they cry wolf?", "Chapter five. The yield curve and the Sahm rule.",
             lit={1998: r"Estrella and Mishkin", 2019: r"Sahm"}, scale=("nation",), horizon=("a year",))
        self.curve()
        self.sahm()
        self.recent()

    def curve(self):
        P = load("probit")
        t = np.array([_t(k) for k in P["months"]])
        sp, pr = np.array(P["spread"]), np.array(P["prob"])
        top = plane([1959, 2027], [-3, 5], center=UP * 1.3 + LEFT * 1.2, x_length=10.6, y_length=2.6,
                    xticks=[1960, 1980, 2000, 2020], yticks=[-2, 0, 2, 4], xlabel=r"",
                    ylabel=r"10-year minus 3-month, \ points", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=12)
        bot = plane([1959, 2027], [0, 1], center=DOWN * 2.0 + LEFT * 1.2, x_length=10.6, y_length=2.2,
                    xticks=[1960, 1980, 2000, 2020], yticks=[0, 0.5, 1], xlabel=r"",
                    ylabel=r"chance of recession in 12 months", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=12)
        rec_t = shade(top, P["spans"], -3, 5, RECESS, 0.55)
        rec_b = shade(bot, P["spans"], 0, 1, RECESS, 0.55)
        z = DashedLine(top.ax.c2p(1959, 0), top.ax.c2p(2027, 0), color=GREY_C, stroke_width=1.2)
        ls = path(top, t, sp, NOW, 1.8, smooth=False)
        lp = path(bot, t, pr, GB, 2.2, smooth=False)
        eq = MathTex(r"\Pr(\text{recession}_{t+12}) = \Phi\big(" + f"{P['b'][0]:.2f}" +
                     r" " + f"{P['b'][1]:+.2f}" + r"\, \text{spread}_t\big)", font_size=26, color=GB)
        side = VGroup(
            eq,
            label(rf"area under the ROC curve: \ {P['auc']:.2f}", font_size=18, color=GB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.25).shift(DOWN * 1.0)
        eps = P["episodes"]
        hit = [e for e in eps if e["recession_after"] is not None]
        tbl = label(rf"inversions of 3 months or more: \ {len(eps)}; \\ followed by a recession within 2 years: \ "
                    rf"{len(hit)}", font_size=18, color=NOW).to_edge(RIGHT, buff=0.25).shift(UP * 1.6)
        tag = data_tag(r"FRED: \ GS10, \ TB3MS, \ USREC", corner=DR, font_size=12)
        with self.voiceover(
            "The most famous recession signal is the slope of the yield curve. <bookmark mark='a'/> In pink, the "
            "ten-year Treasury yield minus the three-month bill rate, with the recessions shaded. Before almost "
            "every recession since the 1960s, it went below zero: long rates under short ones, an inverted curve. "
            "<bookmark mark='b'/> Arturo Estrella and Frederic Mishkin turned it into a probability with a probit: "
            "the chance that the economy is in recession twelve months from now, given today's slope. Fitted to "
            f"every month since 1959, it ranks recession months above others {100 * P['auc']:.0f} percent of the "
            "time. <bookmark mark='c'/> Count the inversions that lasted at least three months: "
            f"{len(eps)}. {len(hit)} were followed by a recession within two years; the exceptions are 1966 and "
            "the long inversion of 2022 to 2024. And one of the hits, 2019, was followed by a pandemic, which no "
            "yield curve predicted."
        ) as vo:
            self.play(FadeIn(top), FadeIn(rec_t), FadeIn(z), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ls), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(bot), FadeIn(rec_b), Create(lp), FadeIn(side), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(tbl))
        self.clear_scene()

    def sahm(self):
        S = load("sahm")
        t = np.array([_t(k) for k in S["rt_months"]])
        v = np.array(S["rt"], float)
        ax = plane([1959, 2027], [-0.5, 4.0], center=LEFT * 1.4 + DOWN * 0.2, x_length=10.2, y_length=4.8,
                   xticks=[1960, 1980, 2000, 2020], yticks=[0, 0.5, 2, 4], xlabel=r"",
                   ylabel=r"Sahm indicator, \ real time, \ points", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:g}", font_size=13)
        rec = shade(ax, S["spans"], -0.5, 4.0, RECESS, 0.55)
        thr = DashedLine(ax.ax.c2p(1959, 0.5), ax.ax.c2p(2027, 0.5), color=ERR, stroke_width=1.8)
        line = path(ax, t, np.clip(v, -0.5, 4.0), SPF, 1.8, smooth=False)
        trig = S["rt_triggers"]
        marks = VGroup()
        for tr in trig:
            x = _t(tr["month"])
            marks.add(Triangle(color=ERR if tr["recession"] is None else GAIN, fill_opacity=1).scale(0.09).rotate(
                PI).move_to(ax.ax.c2p(x, 3.7)))
        false = [tr["month"] for tr in trig if tr["recession"] is None]
        side = VGroup(
            MathTex(r"\bar u_t - \min_{t-12 \le s < t} \bar u_s \ \ge\ 0.5", font_size=26, color=SPF),
            label(r"$\bar u$: \ the three-month average \\ unemployment rate", font_size=17, color=GREY_A),
            label(rf"signals: \ {len(trig)}; \ green near a recession, \\ red without one: \ "
                  rf"{', '.join(f[:4] for f in false)}", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.25)
        tag = data_tag(r"FRED: \ SAHMREALTIME, \ USREC", corner=DR, font_size=12)
        with self.voiceover(
            "The second signal reads unemployment. <bookmark mark='a'/> Claudia Sahm proposed it in 2019 as a "
            "trigger for automatic payments to households: when the three-month average unemployment rate rises "
            "half a point above its lowest in the previous year, a recession has almost always begun. <bookmark "
            "mark='b'/> Computed with the unemployment rates known at the time, the rule has fired "
            f"{len(trig)} times since 1960. <bookmark mark='c'/> Most signals came within a few months of a "
            f"recession's start. Two did not: in {false[0][:4]}, and in {false[-1][:4]}. It is a rule for "
            "recognizing a recession early, not for forecasting one, and like every rule fitted to a few events, "
            "it can break."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(rec), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), Create(thr))
            vo.wait_until("b")
            self.play(Create(line), run_time=3.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m_, shift=DOWN * 0.1) for m_ in marks], lag_ratio=0.15), FadeIn(side[2]),
                      run_time=2.0)
        self.clear_scene()

    def recent(self):
        P, A = load("probit"), load("anxious")
        p22 = P["peak_2022"]
        inv = [e for e in P["episodes"] if e["from"] >= "2022"][0]
        a = dict(zip(A["quarters"], A["p"]))
        rows = VGroup(
            label(rf"the yield curve inverted from {inv['from'][:4]} to {inv['to'][:4]}: \ {inv['months']} months",
                  font_size=23, color=NOW),
            label(rf"the probit's chance of recession peaked at {100 * p22['prob']:.0f}\% \ ({p22['month'][:4]})",
                  font_size=23, color=GB),
            label(rf"the professional forecasters: \ a {a['2023Q2']:.0f}\% chance of a fall in 2023Q3", font_size=23,
                  color=SPF),
            label(r"the Sahm rule fired in July 2024", font_size=23, color=ERR),
            label(r"no recession has been dated since 2020", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        head = label(r"2022--2024: \ every alarm, \ and no fire", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "And then came the alarms of 2022 to 2024. <bookmark mark='a'/> The yield curve inverted for "
            f"{inv['months']} months, the longest inversion in the data. <bookmark mark='b'/> The probit's chance of "
            f"recession peaked at {100 * p22['prob']:.0f} percent. <bookmark mark='c'/> In the spring of 2023 the "
            f"median professional forecaster put a {a['2023Q2']:.0f} percent chance on a fall in output the next "
            "quarter. <bookmark mark='d'/> In July 2024 the Sahm rule fired. <bookmark mark='e'/> No recession has "
            "been dated since the pandemic's. The economy grew instead. The curve inverted because the Federal "
            "Reserve raised short rates fast to fight inflation, and the Sahm rule fired partly because "
            "unemployment rose as more people looked for work, not only because people lost jobs. Every signal is "
            "a summary of past recessions, and the next one need not look like them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
