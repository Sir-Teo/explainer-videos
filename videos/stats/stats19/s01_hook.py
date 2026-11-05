from __future__ import annotations

import numpy as np

from videos.stats.stats19.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.federalist()
        self.dispute()
        self.upon()
        self.paper_by_paper()
        self.prediction()
        self.objectives()

    def federalist(self):
        tl = timeline(lit=(1964,)).to_edge(UP, buff=0.35)
        hc = history_card(1788, r"\emph{The Federalist}, \ New York",
                          r"85 essays urging ratification of the Constitution, \ all signed ``Publius'': \ by Alexander Hamilton, "
                          r"James Madison and John Jay", color=HAM, width=10.4, font_size=24).move_to([0, 1.1, 0])
        rows = fit_rows(VGroup(
            label(r"who wrote which?", font_size=26),
            label(r"both Hamilton and Madison later left lists, \ and the lists disagreed", font_size=24, color=RES),
        ), 12.4, 0.3, [0, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1787 and 1788, eighty-five essays appeared in New York newspapers urging the state to "
            "ratify the new Constitution. All were signed Publius. They were written by Alexander Hamilton, James Madison and "
            "John Jay, and as The Federalist they became a founding text of American government. <bookmark mark='b'/> But "
            "who wrote which? <bookmark mark='c'/> Hamilton, shortly before the duel that killed him, left a list of his "
            "authorship. Madison later left another. The lists disagreed about twelve papers."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def dispute(self):
        d = load("rates")
        cells = VGroup()
        auth = {}
        from explainer.stats import museum as M
        for p in M.federalist()["papers"]:
            auth[p["no"]] = p["author"]
        cols = {"HAMILTON": HAM, "MADISON": MAD, "JAY": GREY_B, "JOINT": S.ALT, "DISPUTED": DISP}
        for i in range(85):
            r, c = divmod(i, 17)
            sq = Square(0.52, stroke_width=1, stroke_color="#101418", fill_color=cols[auth[i + 1]], fill_opacity=0.9)
            sq.move_to([(c - 8) * 0.6, 1.6 - r * 0.6, 0])
            cells.add(VGroup(sq, MathTex(str(i + 1), font_size=16, color="#101418").move_to(sq)))
        key = VGroup(*[VGroup(Square(0.25, stroke_width=0, fill_color=cols[k], fill_opacity=0.9),
                              label(t, font_size=20, color=cols[k])).arrange(RIGHT, buff=0.12)
                       for k, t in (("HAMILTON", r"Hamilton, \ 51"), ("MADISON", r"Madison, \ 14"), ("JAY", r"Jay, \ 5"),
                                    ("JOINT", r"joint, \ 3"), ("DISPUTED", r"disputed, \ 12"))]).arrange(RIGHT, buff=0.5)
        key.move_to([0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are the eighty-five papers. By the consensus of historians, Hamilton wrote fifty-one, "
            "Madison fourteen, Jay five, and three were joint work. <bookmark mark='b'/> The twelve in gold are disputed: "
            "numbers forty-nine to fifty-eight, sixty-two and sixty-three. Historians had argued about them for a century and a "
            "half, by style and by argument, without settling it. The two men wrote in the same formal style, on the same "
            "subjects, often with the same sentence lengths."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.01), FadeIn(key), run_time=2.0)
            vo.wait_until("b")
            self.play(*[Indicate(cells[i - 1], color=DISP) for i in list(range(49, 59)) + [62, 63]])
        self.clear_scene()

    def upon(self):
        d = load("rates")["rates"]
        words = ["upon", "whilst", "while", "enough", "on", "by", "there", "also"]
        A = axes([-0.6, 7.6], [0, 12], x_length=10.0, y_length=4.0, xlabel=r"", ylabel=r"uses per 1,000 words",
                 yticks=[0, 4, 8, 12], center=[0, 0.4, 0])
        ax = A.ax
        w = ax.c2p(0.25, 0)[0] - ax.c2p(0, 0)[0]
        bars = VGroup()
        for k, wd in enumerate(words):
            for j, (au, col) in enumerate((("HAMILTON", HAM), ("MADISON", MAD), ("DISPUTED", DISP))):
                v = min(d[au][wd], 11.9)
                bars.add(Rectangle(width=w, height=max(0.01, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=col,
                                   fill_opacity=0.9).move_to(ax.c2p(k - 0.27 + 0.27 * j, 0), aligned_edge=DOWN))
        names = VGroup(*[label(rf"\emph{{{wd}}}", font_size=22, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                         for k, wd in enumerate(words)])
        key = VGroup(label(r"Hamilton", font_size=22, color=HAM), label(r"Madison", font_size=22, color=MAD),
                     label(r"disputed", font_size=22, color=DISP)).arrange(RIGHT, buff=0.6).move_to([0, 3.0, 0])
        foot = label(r"Mosteller \& Wallace (1964): \ the dull words, \ not the brilliant ones", font_size=24, color=OBS).to_edge(DOWN, buff=0.5)
        tag = historical_tag(r"\emph{The Federalist}, \ Project Gutenberg", corner=UR)
        with self.voiceover(
            "<bookmark mark='a'/> In the 1960s Frederick Mosteller and David Wallace tried something different: count the "
            "dullest words. <bookmark mark='b'/> Here are the rates of a few, per thousand words, in Hamilton's papers, in "
            "Madison's, and in the disputed twelve. Hamilton writes upon three times in every thousand words; Madison, almost "
            "never. Madison writes whilst; Hamilton writes while, and enough. Madison uses on and by far more. "
            "<bookmark mark='c'/> And on every one of these words, the disputed papers look like Madison's. "
            "<bookmark mark='d'/> Function words like these are used without thought, so they're habits rather than choices, "
            "and they don't depend much on the subject."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for k_, b_ in enumerate(bars) if k_ % 3 != 2], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for k_, b_ in enumerate(bars) if k_ % 3 == 2], lag_ratio=0.08))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def paper_by_paper(self):
        d = load("rates")
        A = axes([-0.3, 8.0], [0, 3.5], x_length=9.0, y_length=3.6, xlabel=r"\emph{upon}, \ per 1,000 words, \ paper by paper",
                 xticks=[0, 2, 4, 6, 8], center=[-0.4, 0.6, 0])
        ax = A.ax
        g = np.random.Generator(np.random.PCG64(1964))
        rows_y = {"HAMILTON": 2.8, "MADISON": 1.7, "DISPUTED": 0.6}
        cols = {"HAMILTON": HAM, "MADISON": MAD, "DISPUTED": DISP}
        dots = VGroup()
        for au, y in rows_y.items():
            for v in d["upon"][au]:
                dots.add(Dot(ax.c2p(min(v, 7.9), y + 0.35 * (g.random() - 0.5)), radius=0.07, color=cols[au]))
        names = VGroup(*[label(t, font_size=22, color=cols[au]).next_to(ax.c2p(-0.3, y), LEFT, buff=0.15)
                         for au, y, t in (("HAMILTON", 2.8, r"Hamilton, \ 51"), ("MADISON", 1.7, r"Madison, \ 14"),
                                          ("DISPUTED", 0.6, r"disputed, \ 12"))])
        z = d["upon_zero"]
        rows = fit_rows(VGroup(
            label(rf"Hamilton: \ \emph{{upon}} in every paper", font_size=22, color=HAM),
            label(rf"Madison: \ none at all in {z['MADISON']} of 14", font_size=22, color=MAD),
            label(rf"disputed: \ none in {z['DISPUTED']} of 12", font_size=22, color=DISP),
        ), 12.0, 0.25, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Paper by paper, upon alone nearly separates them. <bookmark mark='b'/> Hamilton used it in every "
            "one of his fifty-one papers, at rates from one to seven and a half per thousand words. <bookmark mark='c'/> Madison didn't "
            "use it at all in eleven of his fourteen. <bookmark mark='d'/> And ten of the twelve disputed papers have no upon "
            "at all. One word is a hint, not a verdict. But Mosteller and Wallace combined dozens of such words in a careful "
            "probability model, and reached a decision we'll reproduce in chapter nine."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in dots[:51]], lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in dots[51:65]], lag_ratio=0.05), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in dots[65:]], lag_ratio=0.05), FadeIn(rows[2]))
        self.clear_scene()

    def prediction(self):
        rows = fit_rows(VGroup(
            label(r"a new goal: \ not a parameter, \ but a prediction", font_size=26),
            label(r"given the words, \ who wrote it?", font_size=24, color=DISP),
            label(r"how good is a rule at predicting cases it hasn't seen?", font_size=24, color=OBS),
            label(r"and how do we know, \ honestly?", font_size=24, color=RES),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> This is a different kind of problem from most of the course so far. The goal isn't a "
            "parameter with an interval, but a prediction: <bookmark mark='b'/> given these word counts, who wrote this paper? "
            "<bookmark mark='c'/> The question that matters is how well a prediction rule works on cases it hasn't seen, "
            "<bookmark mark='d'/> and how to find that out without fooling ourselves."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 19", font_size=34, color=GREY_B), label(r"Learning from Data", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"training and test error; \ overfitting; \ the bias--variance trade-off",
            r"cross-validation and the one-standard-error rule",
            r"nearest neighbours and the curse of dimensionality",
            r"naive Bayes, \ logistic regression and trees; \ ridge and the lasso, \ a first look",
            r"classification metrics, \ the \emph{Federalist} decided, \ and leakage",
        ], color=DISP, font_size=26)
        prereq = note(r"prerequisites: \ Parts 12, \ 14 and 16").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.learn}; \ the $\ell_1$ geometry").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part nineteen: learning from data. <bookmark mark='b'/> We'll separate training error from "
            "test error and see overfitting happen; derive the trade-off between bias and variance; estimate test error by "
            "cross-validation; meet nearest neighbours and the curse of dimensionality; compare naive Bayes with logistic "
            "regression, and grow and prune trees; take a first look at ridge and the lasso; learn the metrics for "
            "classifiers; decide the Federalist; and finish with the many ways an evaluation can leak."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
