from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, BUG, GOOD, HONEST, HURDLE, IS_C, OOS_C, PART, RULE, ask, comma, illustration, load


class PurgedCV(VoiceoverScene):
    def construct(self):
        c = load("cv")
        self.card()
        self.overlap()
        self.experiment(c)
        self.results(c)
        self.purge()
        self.walk()
        self.when(c)
        self.question()

    def card(self):
        c = chapter_card(10, r"Purged cross-validation and walk-forward", r"How does validation leak?", lit=(2018,),
                         part=PART)
        with self.voiceover("Chapter ten. Cross-validation, the machine learner's standard tool, and the two ways it "
                            "leaks on financial time series."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def overlap(self):
        line = NumberLine(x_range=[0, 60, 5], length=12.0, color=GREY_C, include_numbers=False).move_to(UP * 2.0)
        lab = label(r"trading days", font_size=18, color=GREY_A).next_to(line, UP, buff=0.15)
        u = 12.0 / 60
        x0 = line.n2p(0)[0]
        spans = VGroup()
        for k, t in enumerate(range(20, 30)):
            col = OOS_C if t == 25 else (BUG if abs(t - 25) <= 4 else IS_C)
            y = 1.2 - 0.32 * k
            spans.add(VGroup(Dot([x0 + t * u, y, 0], radius=0.05, color=col),
                             Line([x0 + (t + 1) * u, y, 0], [x0 + (t + 21) * u, y, 0], color=col, stroke_width=4)))
        cap = VGroup(
            label(r"each observation: features from the past (the dot), a label from the next 20 days (the bar)",
                  font_size=19),
            label(r"the test day (teal) and its neighbours (red) share 16 to 19 of their 20 label days", font_size=19,
                  color=BUG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Financial labels overlap. <bookmark mark='a'/> A model that forecasts the next twenty days' return makes "
            "one observation a day: its features from the past, its label from the twenty days ahead. Neighbouring "
            "observations share almost all of their label: the day before shares nineteen of its twenty days. "
            "<bookmark mark='b'/> Shuffle the observations into random folds, as ordinary cross-validation does, and "
            "nearly every test day has its neighbours in the training set, with almost the same features and almost "
            "the same answer. The model does not need to forecast. It only needs to remember yesterday."
        ) as vo:
            self.play(Create(line), FadeIn(lab))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.1) for s_ in spans], lag_ratio=0.12), FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(FadeIn(cap[1]), Indicate(spans[5], color=OOS_C))
        self.wait(0.4)
        self.clear_scene()

    def experiment(self,c):
        rows=[cmath(r"\ell_t",r"=",r"\log(1+r_t),\quad x_t=(\ell_t,\sum_{j=0}^{4}\ell_{t-j},\sum_{j=0}^{19}\ell_{t-j},\sum_{j=0}^{59}\ell_{t-j},\hat\sigma_{20,t})",font_size=29,colors={r"\ell_t":RULE}),
              cmath(r"y_t",r"=",r"\sum_{j=1}^{20}\ell_{t+j}",font_size=37,colors={r"y_t":HURDLE}),
              cmath(r"\hat y_t",r"=",r"{1\over25}\sum_{j\in\text{25 nearest training features}}y_j",font_size=34,colors={r"\hat y_t":OOS_C})]
        whys=[why(r"the unchanged code standardises features using full-sample means and standard deviations before splitting: every saved validation result therefore includes scaling leakage"),
              why(rf"next 20-day log return; {c['first']//10000}--{c['last']//10000}; {comma(c['n'])} overlapping observations"),
              why(r"$R^2$ uses the training mean as benchmark; hit rate classifies above/below the training label median, not simply positive/negative return")]
        step=ladder(self,rows,whys,keep=3,top=2.9,x=-.5,buff=.45,edge=6.9)
        with self.voiceover("The unchanged nearest-neighbour experiment is useful because its limitations can be traced. <bookmark mark='a'/> It uses one-, five-, twenty- and sixty-day log returns and recent volatility. But it standardises every feature once using the full sample, before any split. That leaks scaling information into all the saved validation results. <bookmark mark='b'/> The target is the next twenty trading days' log return, so adjacent labels overlap. <bookmark mark='c'/> Predictions average twenty-five nearby training labels. R squared compares with the training mean, while hit rate classifies above or below the training label median. These are diagnostic scores, not certified real-time forecast estimates.") as vo:
            step(0);vo.wait_until('a');self.wait(.1);vo.wait_until('b');step(1);vo.wait_until('c');step(2)
        self.clear_scene()

    def results(self, c):
        R = c["res"]
        items = [(r"shuffled 5-fold", R["shuffled"], BUG), (r"blocked 5-fold", R["blocked"], IS_C),
                 (r"purged and embargoed", R["purged"], HONEST), (r"walk-forward", R["walk"], OOS_C)]
        g = VGroup()
        for i, (nm, r, col) in enumerate(items):
            v = 100 * r["r2"]
            b = Rectangle(width=abs(v) * 0.55, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([v * 0.275, 1.4 - 0.85 * i, 0])
            g.add(VGroup(label(nm, font_size=20, color=col).move_to([-5.2, 1.4 - 0.85 * i, 0]), b,
                         MathTex(rf"{v:+.1f}\%", font_size=24).next_to(b, RIGHT if v > 0 else LEFT, buff=0.12),
                         MathTex(rf"\text{{hit}}\ {100 * r['hit']:.1f}\%", font_size=22, color=GREY_A).move_to(
                             [5.0, 1.4 - 0.85 * i, 0])))
        axis = Line([0, 1.8, 0], [0, -1.6, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"Original validation scores: remaining leakage matters", font_size=26).to_edge(UP, buff=0.4)
        foot = wrapped_label(r"All scores use full-sample feature scaling. Blocked/purged folds include future training; walk-forward leaves overlapping boundary labels. These are original diagnostics, not clean live-performance estimates.", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"The original saved scores differ across validation schemes. <bookmark mark='a'/> Shuffling reports R squared {100*R['shuffled']['r2']:.1f} percent and hit rate {100*R['shuffled']['hit']:.1f} percent. Adjacent overlapping labels can make that comparison optimistic. <bookmark mark='b'/> Blocked, purged and walk-forward R squared are {100*R['blocked']['r2']:.1f}, {100*R['purged']['r2']:.1f} and {100*R['walk']['r2']:.1f} percent. <bookmark mark='c'/> These differences do not identify a causal effect or prove all forecasting impossible. Full-sample scaling remains in every score. Blocked and purged folds use future observations, and walk-forward retains labels that mature inside its test period."
        ) as vo:
            self.play(FadeIn(head), Create(axis))
            vo.wait_until("a")
            self.play(FadeIn(g[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in g[1:]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.add(illustration(r"Ken French daily market, 1963--2020; the House's \texttt{backtest.purged\_kfold}"))
        self.wait(0.4)
        self.clear_scene()

    def purge(self):
        n = 40
        W = 12.0 / n
        x0 = -6.0
        row = VGroup()
        for i in range(n):
            col = OOS_C if 16 <= i < 24 else (BAD if 12 <= i < 16 else (HURDLE if 24 <= i < 28 else IS_C))
            row.add(Rectangle(width=W * 0.92, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.75).move_to(
                [x0 + (i + 0.5) * W, 1.0, 0]))
        tags = VGroup(
            label(r"train", font_size=18, color=IS_C).next_to(row[5], UP, buff=0.15),
            label(r"purged", font_size=18, color=BAD).next_to(row[13], UP, buff=0.15),
            label(r"test", font_size=18, color=OOS_C).next_to(row[19], UP, buff=0.15),
            label(r"embargo", font_size=18, color=HURDLE).next_to(row[25], UP, buff=0.15),
            label(r"train", font_size=18, color=IS_C).next_to(row[33], UP, buff=0.15),
        )
        notes = VGroup(
            label(r"purge: drop every training observation whose label period overlaps the test fold's", font_size=19,
                  color=BAD),
            label(r"embargo: also drop a gap after the test fold, as long as the label (here 20 days)", font_size=19,
                  color=HURDLE),
            label(r"a 20-day gap does not remove all 60-day feature overlap; future-fold training also differs from live prediction", font_size=19),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(row, DOWN, buff=0.7)
        with self.voiceover(
            "Contiguous folds still leak at their edges, and Marcos Lopez de Prado's fix has two parts. "
            "<bookmark mark='a'/> Purge: remove from training every observation whose label period overlaps the test "
            "fold's, so no training answer contains a test day. <bookmark mark='b'/> Embargo: also remove a gap "
            "after the test fold. Its length must reflect the information carried by labels and features, not just one convenient horizon. This code uses a twenty-day embargo but features look back sixty days. Purging does not repair full-sample preprocessing or turn future-fold training into a historical deployment simulation."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_) for r_ in row], lag_ratio=0.01), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), Indicate(VGroup(*row[12:16]), color=BAD))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), Indicate(VGroup(*row[24:28]), color=HURDLE), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def walk(self):
        rows = VGroup()
        for k in range(5):
            tr = 8 + 6 * k
            r_ = VGroup()
            for i in range(40):
                col = IS_C if i < tr else (OOS_C if i < tr + 6 else GREY_D)
                r_.add(Rectangle(width=0.28, height=0.32, stroke_width=0, fill_color=col,
                                 fill_opacity=0.8 if i < tr + 6 else 0.25))
            rows.add(r_.arrange(RIGHT, buff=0.02))
        rows.arrange(DOWN, buff=0.15).move_to(UP * 0.5)
        notes = VGroup(
            label(r"fit on everything before; test on what comes next; step forward and refit", font_size=20),
            label(r"chronological fitting is necessary for a replay; mature every training label and fit all preprocessing only on available training data", font_size=19, color=GREY_A),
            label(r"its weakness: one path through history, so few test periods and noisy scores", font_size=19,
                  color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(rows, DOWN, buff=0.5)
        with self.voiceover(
            "A walk-forward design fits on earlier observations and tests later ones. <bookmark mark='a'/> A real replay must also wait for training labels to mature, fit scaling only on the available training data, and keep model choices separate from the final evaluation. The saved implementation splits feature timestamps chronologically but leaves overlapping twenty-day training labels at the test boundary. <bookmark mark='b'/> Its negative score is an illustrative original result with residual leakage. Chronology alone neither removes those leaks nor guarantees performance through a future regime change."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.25), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def when(self, c):
        R = c["res"]
        cards = VGroup(
            desk_question(r"saved score differences have limited scope", rf"all folds use leaked full-sample scaling; future training remains. "
                          rf"purging removed {R['purged']['dropped']:.0f} per fold ({comma(c['n'])} total observations) and changed "
                          rf"$R^2$ by less than a tenth of a point. With 20 folds it removed {R['purged20']['dropped']:.0f} a fold", width=12.2,
                          font_size=19),
            desk_question(r"purging matters more when", r"labels are long (a year's return, a default within three years), "
                          r"folds are many, or the features themselves are smoothed over long windows", width=12.2,
                          font_size=19),
            desk_question(r"choose a split for the target", r"future forecasts require availability and label maturity; random splitting answers a different target when neighbours "
                          r"are dependent or labels overlap", width=12.2, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            f"Read these scores with their remaining leaks in view. <bookmark mark='a'/> The five-fold purged calculation drops an average {R['purged']['dropped']:.0f} training observations per fold, and the twenty-fold version {R['purged20']['dropped']:.0f}. Small score differences here do not establish that leakage is unimportant. All methods use full-sample scaling; the blocked and purged designs can train on future observations. <bookmark mark='b'/> Purging removes specified overlapping label intervals. A suitable gap also depends on feature lookbacks, label maturity and the evaluation target. <bookmark mark='c'/> For a future trading forecast use a chronological, available-time protocol. Random splitting can answer a different exchangeable-sample question, but it does not validate that live forecasting claim."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a credit model labels each firm-year by whether the firm defaults in the next three years, and is "
                r"validated with five random folds of firm-years. Where is the leak, and what is the fix?")
        with self.voiceover(
            "Pause and predict. A credit model labels each firm-year by whether the firm defaults within three years, "
            "and is validated with five random folds of firm-years. Where is the leak, and what is the fix?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
