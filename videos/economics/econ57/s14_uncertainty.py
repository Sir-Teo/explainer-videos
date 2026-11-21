from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403

ORD = {"1": "first", "2": "second", "3": "third", "4": "fourth"}


class Uncertainty(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Telling people about uncertainty", r"How should a forecaster tell people who want a "
             r"number?", "Chapter twelve. Telling people about uncertainty.",
             lit={1996: r"the Bank of England's fan chart"}, scale=("person", "nation"), horizon=("a year",))
        self.fan()
        self.words()

    def fan(self):
        S = load("score")
        rows = S["rows"]
        f = np.array(S["latest_forecast"], float)
        h = np.arange(len(f))
        q = np.array([r["q"] for r in rows])             # error quantiles: 5, 25, 50, 75, 95
        # the outcome is the forecast minus the error, so the error's upper tail is the outcome's lower tail
        lo95, lo50 = f - q[:, 4], f - q[:, 3]
        hi50, hi95 = f - q[:, 1], f - q[:, 0]
        ax = plane([-0.3, 4.3], [-6, 9], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=5.2,
                   xticks=[0, 1, 2, 3, 4], yticks=[-4, 0, 4, 8], xlabel=r"quarters after the survey",
                   ylabel=r"real GDP growth, \ \% a year", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        z = DashedLine(ax.ax.c2p(-0.3, 0), ax.ax.c2p(4.3, 0), color=GREY_C, stroke_width=1.2)
        b95 = band(ax, h, lo95, hi95, SPF, 0.2)
        b50 = band(ax, h, lo50, hi50, SPF, 0.45)
        cen = path(ax, h, f, WHITE, 3.0, smooth=False)
        side = VGroup(
            label(rf"white: \ the professional forecasters, \\ {S['latest_survey']} survey", font_size=18,
                  color=WHITE),
            label(r"dark band: \ half of past errors", font_size=18, color=SPF),
            label(r"light band: \ nine in ten", font_size=18, color=SPF),
            label(r"the bands come from the record, \\ not from a model", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        p_neg = []
        for k in range(len(f)):
            e = np.array(rows[k]["fc"]) - np.array(rows[k]["act"])
            p_neg.append(float(np.mean(f[k] - e < 0)))
        tag = data_tag(r"Philadelphia Fed: \ SPF; \ errors against first estimates, \ 1968--2026", corner=DR,
                       font_size=12)
        with self.voiceover(
            "A forecast without its uncertainty invites false confidence. <bookmark mark='a'/> Here is the latest "
            f"professional forecast, from the survey of the {ORD[S['latest_survey'][-1]]} quarter of "
            f"{S['latest_survey'][:4]}: growth of about {f[0]:.1f} percent a year, and about {f[-1]:.1f} a year on. "
            "<bookmark "
            "mark='b'/> Around it, the forecasters' own record: the band holding half of their past errors at each "
            "horizon, <bookmark mark='c'/> and the band holding nine in ten. A year ahead the wider band runs from "
            f"{say_num(lo95[-1], 1)} to {say_num(hi95[-1], 1)} percent. <bookmark mark='d'/> Read that way, the "
            f"record says there is about a {100 * p_neg[-1]:.0f} percent chance that growth a year ahead will be "
            "negative, though the forecast itself will never say so. The Bank of England has drawn its forecasts "
            "this way since 1996, as a fan."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(z), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cen), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(b50), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(b95), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def words(self):
        rows = VGroup(
            label(r"`likely' \ means 66 to 100\% \quad (the IPCC's calibrated language)", font_size=23, color=SPF),
            label(r"a fan chart's centre is read as the forecast; \ its edges are ignored", font_size=23,
                  color=FIRST),
            label(r"scenarios tell stories; \ but which story is likeliest?", font_size=23, color=GB),
            label(r"say the number, \ the range, \ and what would change your mind", font_size=25,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"words, \ fans and stories", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "How to say it in words? <bookmark mark='a'/> The climate scientists of the IPCC tie their words to "
            "numbers: 'likely' means a probability of at least two in three. <bookmark mark='b'/> Fan charts have "
            "a known weakness: readers look at the centre and ignore the edges; Bernanke judged that they conveyed "
            "little useful information, and recommended scenarios instead. <bookmark mark='c'/> Scenarios have "
            "the opposite weakness: they tell "
            "stories without saying which is likeliest. <bookmark mark='d'/> The practical rule is simple: give the "
            "number, the range, and what would change your mind."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
