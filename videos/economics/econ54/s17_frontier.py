from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ learned estimators", r"Can a machine learn to estimate?",
             "Chapter fifteen. Frontier: learned estimators.",
             lit={2020: r"Cranmer, Brehmer and Louppe", 2023: r"Horton"}, scale=("person", "world"),
             horizon=("a decade",))
        self.amortized()
        self.open_()

    def amortized(self):
        A = load("amortized")
        ax = plane([-1, 1], [-1, 1], center=LEFT * 2.2 + DOWN * 0.3, x_length=5.0, y_length=5.0,
                   xticks=[-0.8, -0.4, 0, 0.4, 0.8], yticks=[-0.8, -0.4, 0, 0.4, 0.8], xlabel=r"the true $\theta$",
                   ylabel=r"the learned estimate", xfmt=lambda v: f"{v:.1f}".replace("-", "{-}"),
                   yfmt=lambda v: f"{v:.1f}".replace("-", "{-}"), font_size=13)
        diag = DashedLine(ax.ax.c2p(-1, -1), ax.ax.c2p(1, 1), color=GREY_C, stroke_width=1.4)
        pts = VGroup(*[dot(ax, x, y, EST, 0.035) for x, y in zip(A["theta"], A["pred"])])
        steps = flow_chain(steps=[(r"draw a parameter", MODEL), (r"simulate a data set", MODEL),
                                  (r"summarize it", DATA), (r"learn the map from summaries back", EST)],
                           direction=DOWN, box_w=3.4, box_h=0.75, font_size=17, buff=0.3).to_edge(RIGHT, buff=0.6)
        steps.shift(UP * 0.6)
        notes = VGroup(
            label(rf"{A['train']:,} simulated samples to learn from; \\ then {len(A['theta'])} new ones: \ error "
                  rf"{A['rmse']:.3f}", font_size=18, color=EST),
            label(r"once learned, \ each new estimate is instant", font_size=18, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(steps, DOWN, buff=0.45)
        tag = published_tag(r"Cranmer, \ Brehmer and Louppe, \ PNAS 117(48) (2020)", corner=DR, font_size=12)
        with self.voiceover(
            "Simulated moments search for the parameters anew for every data set. The frontier turns that around. "
            "<bookmark mark='a'/> Draw a parameter at random, <bookmark mark='b'/> simulate a data set from the "
            "model, <bookmark mark='c'/> summarize it, and do this thousands of times. <bookmark mark='d'/> Then "
            "learn the map from summaries back to the parameter that produced them: with a regression here, with "
            "a neural network at scale. <bookmark mark='e'/> For the moving average, after "
            f"{A['train']:,} simulated samples, the learned map estimates {len(A['theta'])} fresh ones with a "
            f"typical error of {A['rmse']:.2f}, and each estimate takes no search at all. Kyle Cranmer, Johann "
            "Brehmer and Gilles Louppe call the family simulation-based inference; it learns whole posterior "
            "distributions, not just points, and economists have begun to use it for structural models whose "
            "simulations are too slow to search through."
        ) as vo:
            self.play(FadeIn(ax), Create(diag), FadeIn(tag))
            for mk, k in zip("abcd", range(4)):
                vo.wait_until(mk)
                an = [FadeIn(steps.boxes[k], shift=DOWN * 0.1)]
                if k > 0:
                    an.append(Create(steps.arrows[k - 1]))
                self.play(*an)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.005), FadeIn(notes), run_time=2.0)
        self.clear_scene()

    def open_(self):
        cards = point_cards([
            (r"learned estimators", r"fast, \ and approximate: \ their own errors need checking against the truth, "
             r"\ as the Island allows", EST),
            (r"machine learning inside", r"flexible first stages and nuisance functions, \ with the structural "
             r"parameter kept in view", PATIENCE),
            (r"models meet experiments", r"estimate on one arm, \ predict the other; \ or let an experiment "
             r"identify what the model cannot", GAIN),
            (r"simulated people", r"language models as survey respondents and players of games: \ a source of "
             r"hypotheses, \ not of parameters, \ until validated", CAUTION),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Horton, \ NBER WP 31122 (2023)", corner=DR, font_size=12)
        with self.voiceover(
            "What remains open. <bookmark mark='a'/> Learned estimators are fast but approximate, and their errors "
            "have to be checked against known truths, which is what a simulated world like the Island is for. "
            "<bookmark mark='b'/> Machine learning is moving inside estimation: flexible models for the parts of a "
            "problem we do not care about, with the structural parameter kept in view. <bookmark mark='c'/> Models "
            "and experiments are being combined: estimate on one arm and predict the other, as Todd and Wolpin did, "
            "or let an experiment pin down the parameter the observational data cannot. <bookmark mark='d'/> And "
            "John Horton and others have asked language models to answer surveys and play economic games, as "
            "simulated people. Whether their answers say anything about real people's parameters is, so far, a "
            "question for validation, not an answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
