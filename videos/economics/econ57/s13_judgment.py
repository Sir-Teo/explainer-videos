from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403


class Judgment(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Judgment, \ models and combinations", r"Should a forecaster trust the model, \ the "
             r"judgment, \ or both?", "Chapter eleven. Judgment, models and combinations.",
             lit={1969: r"Bates and Granger", 2004: r"Stock and Watson", 2024: r"the Bernanke review"},
             scale=("firm", "nation"), horizon=("a year",))
        self.combine()
        self.scenarios()

    def combine(self):
        G = load("greenbook")
        rows = G["rows"]
        eq = MathTex(r"f^c = w\, f^{\text{staff}} + (1 - w)\, f^{\text{SPF}}, \qquad w^* = \arg\min_w\ "
                     r"\textstyle\sum (f^c - a)^2", font_size=32, color=WHITE).to_edge(UP, buff=0.5)
        hdr = VGroup(*[label(t_, font_size=19, color=c_) for t_, c_ in
                       ((r"quarters ahead", GREY_A), (r"staff", GB), (r"SPF", SPF), (r"half and half", LATEST),
                        (r"best $w$", E.ACCENT), (r"errors' correlation", GREY_A))])
        xs = [-5.0, -2.6, -1.0, 0.7, 2.6, 4.7]
        table = VGroup()
        for k, h_ in enumerate(hdr):
            h_.move_to([xs[k], 1.3, 0])
        for j, r in enumerate(rows):
            y = 0.6 - 0.55 * j
            vals = [f"{r['h']}", f"{r['rmse_gb']:.2f}", f"{r['rmse_spf']:.2f}", f"{r['rmse_avg']:.2f}",
                    f"{r['w_gb']:.2f}", f"{r['corr']:.2f}"]
            row = VGroup(*[label(v_, font_size=21, color=WHITE if k else GREY_A).move_to([xs[k], y, 0])
                           for k, v_ in enumerate(vals)])
            best = int(np.argmin([r["rmse_gb"], r["rmse_spf"], r["rmse_avg"]])) + 1
            row[best].set_color(E.ACCENT)
            table.add(row)
        foot = label(r"inflation forecasts, \ root mean squared errors; \ gold: \ the lowest in each row",
                     font_size=17, color=GREY_B).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "If two forecasts are both informative, why choose? <bookmark mark='a'/> In 1969 John Bates and Clive "
            "Granger showed that a weighted average of two forecasts can beat both, when their errors are not "
            "perfectly correlated. <bookmark mark='b'/> Take the staff's and the professional forecasters' "
            "inflation forecasts from the last chapter. <bookmark mark='c'/> For the current quarter, half and half "
            f"has the lowest error, {rows[0]['rmse_avg']:.2f}, and the best weight on the staff is about "
            f"{rows[0]['w_gb']:.2f}. <bookmark mark='d'/> Further ahead the two forecasts' errors are correlated "
            f"{rows[-1]['corr']:.2f}, the staff's are smaller, and the best weight goes to {rows[-1]['w_gb']:.2f}: "
            "averaging only helps when the forecasters know different things. In practice, James Stock and Mark "
            "Watson found that simple averages usually beat weights estimated from a short history, the "
            "forecast-combination puzzle: estimated weights fit the past too well."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(eq), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(hdr), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(table[0], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in table[1:]], lag_ratio=0.3),
                      run_time=2.0)
        self.clear_scene()

    def scenarios(self):
        cards = point_cards([
            (r"judgment", r"forecasters adjust models by hand: \ for strikes, \ storms, \ a pandemic, \ or news the "
             r"model has never seen; \ the adjustment should be written down and scored too", GB),
            (r"scenarios", r"not one forecast but a few coherent stories: \ what if oil doubles, \ what if credit "
             r"tightens; \ each with its policy", SPF),
            (r"the Bernanke review, \ 2024", r"asked to review the Bank of England's forecasting, \ Ben Bernanke "
             r"made twelve recommendations: \ modernize the models and data, \ publish alternative scenarios, \ and "
             r"drop the fan chart", E.ACCENT),
        ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.1)
        tag = published_tag(r"Bernanke, \ `Forecasting for monetary policy making and communication at the Bank "
                            r"of England: \ a review' (April 2024)", corner=DR, font_size=11)
        with self.voiceover(
            "Models are never left alone. <bookmark mark='a'/> Forecasters adjust them by judgment, for a strike, "
            "a storm, a pandemic, or news the model has never seen; the adjustment should be written down, and "
            "scored like any forecast. <bookmark mark='b'/> And one number is often less useful than a few "
            "coherent stories: what happens if oil doubles, or credit tightens, and what policy each would call "
            "for. <bookmark mark='c'/> In April 2024 Ben Bernanke, asked to review the Bank of England's forecasting "
            "after it missed the inflation of 2021 and 2022, made twelve recommendations: rebuild the models and "
            "data, publish alternative scenarios, and drop the fan chart the Bank had used for nearly thirty years. "
            "Which brings us to how uncertainty should be told."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
