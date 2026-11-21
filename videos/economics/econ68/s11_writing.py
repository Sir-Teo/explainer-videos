from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403


class Writing(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Writing it, \ and the referees", r"How does a result become a paper that others can check?",
             "Chapter nine. Writing it, and the referees.", scale=("world",), horizon=("a year",))
        self.introduction()
        self.referees()

    def introduction(self):
        D, Bu, C = load("did"), load("buses"), load("clock")
        j9 = 100 * (np.exp(C["nine"]["jump"]) - 1)
        paras = VGroup(
            label(r"1. \ the question, \ and why it matters: \ the first downtown charge in the United States",
                  font_size=20, color=FIRST),
            label(r"2. \ what we do: \ three designs on public data, \ with placebo years", font_size=20,
                  color=TRUE),
            label(rf"3. \ what we find: \ tunnels {100 * D['adjusted']:.1f}\% net of their drift; \ buses "
                  rf"{100 * Bu['effect']:+.1f}\%; \ entries +{j9:.0f}\% the minute the toll falls".replace("-",
                                                                                                         "{-}"),
                  font_size=20, color=DATA),
            label(r"4. \ why it differs from the official figure, \ and what the designs cannot say", font_size=20,
                  color=TOLL),
            label(r"5. \ the model, \ the counterfactual, \ and what it leaves out", font_size=20, color=MODEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.1)
        head = label(r"the introduction is an argument, \ in five paragraphs", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "A paper is read from its introduction, so the introduction is the argument in miniature. <bookmark "
            "mark='a'/> First the question and why it matters. <bookmark mark='b'/> Then what the paper does. "
            "<bookmark mark='c'/> Then what it finds, with the numbers. <bookmark mark='d'/> Then the honest part: "
            "why the answer differs from the official figure, and what the designs cannot say. <bookmark "
            "mark='e'/> Then the model, the counterfactual, and what they leave out. A talk follows the same five "
            "steps, in twenty minutes, with one picture for each."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcde", paras):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def referees(self):
        cards = point_cards([
            (r"Referee 1", r"`the tunnels' drift could be the pandemic's long tail: \ show it does not depend on the "
             r"placebo years chosen'", TOLL),
            (r"the reply", r"the drift is estimated from 2023 and 2024 alone, \ and again from 2024 alone; \ the "
             r"net effect is reported both ways", TRUE),
            (r"Referee 2", r"`diversion to the free bridges is the first-order question: \ what bounds can you "
             r"put on it?'", CTRL),
            (r"the reply", r"none from this data; \ the Island in the next chapter shows the direction of the "
             r"bias, \ and the paper says so", MODEL),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"the referees, \ and the reply", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Then the referees, the colleagues an editor asks to find what is wrong. <bookmark mark='a'/> The first "
            "asks whether the tunnels' drift is the pandemic's long tail, and whether the result depends on which "
            "years are the placebos. <bookmark mark='b'/> The reply does the work: estimate the drift from 2023 and "
            "2024, then from 2024 alone, and report both. <bookmark mark='c'/> The second asks the hardest question: "
            "how much traffic moved to the free bridges, which this data cannot see? <bookmark mark='d'/> The honest "
            "reply is that this data cannot bound it; a model can show which way the bias runs, and the paper must "
            "say so. Most of a paper's quality is made in replies like these."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
