from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403


class Writing(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Writing it, \ and the referees", r"How does a result become a paper that others can check?",
             "Chapter nine. Writing it, and the referees.", scale=("world",), horizon=("a year",))
        self.introduction()
        self.referees()
        self.replies()

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
            (r"the reply", r"the drift is estimated from 2023 and 2024, \ and again from 2024 alone; \ the net "
             r"effect is reported both ways", TRUE),
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

    def replies(self):
        D = load("did")
        nm = D["no_manhattan"]
        rows_ = [(r"the paper: \ drift from 2023--2024", D["adjusted"], TOLL),
                 (r"drift from 2024 alone", D["adjusted_2024"], DATA),
                 (rf"controls without the bridges \\ that also serve Manhattan ({nm['n_controls']})", nm["adjusted"],
                  CTRL)]
        ax = plane([-3, 1], [0, 3.6], center=RIGHT * 1.6 + DOWN * 0.2, x_length=7.0, y_length=4.0,
                   xticks=[-3, -2, -1, 0, 1], yticks=[], xlabel=r"the charge's effect on the tunnels, \ \%",
                   xfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        zero = vline(ax, 0, 0, 3.6, GREY_C, 1.4)
        se = 100 * D["se_adjusted"]
        marks, names = VGroup(), VGroup()
        for k, (nm_, v, col) in enumerate(rows_):
            y = 3.0 - 1.0 * k
            m = 100 * v
            bar = Line(ax.ax.c2p(m - 1.96 * se, y), ax.ax.c2p(m + 1.96 * se, y), stroke_color=col, stroke_width=6,
                       stroke_opacity=0.6)
            d = Dot(ax.ax.c2p(m, y), radius=0.09, color=WHITE)
            t = label(rf"{m:.1f}\%".replace("-", "{-}"), font_size=16, color=col).next_to(d, UP, buff=0.12)
            marks.add(VGroup(bar, d, t))
            names.add(label(nm_, font_size=16, color=col).next_to(ax.ax.c2p(-3, y), LEFT, buff=0.25))
        foot = label(r"the interval is the main estimate's: \ the answers move inside it", font_size=17,
                     color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"the replies, \ in numbers", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.45)
        tag = data_tag(r"MTA crossings; \ agora.congestion.yoy\_did", corner=DL, font_size=12)
        with self.voiceover(
            "And the replies, in numbers. <bookmark mark='a'/> The paper's estimate: net of the drift measured over "
            f"2023 and 2024, {say_pct(-D['adjusted'], 1)}. <bookmark mark='b'/> With the drift measured from 2024 "
            f"alone, as the first referee asked, {say_pct(-D['adjusted_2024'], 1)}. <bookmark mark='c'/> Dropping "
            "the two bridges whose traffic also flows into Manhattan from the comparison group, "
            f"{say_pct(-nm['adjusted'], 1)}. <bookmark mark='d'/> Every answer sits inside the main estimate's "
            "interval. The result is small and steady; what remains uncertain is diversion, and the paper says so."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(zero), FadeIn(tag))
            for mk, mk_, n_ in zip("abc", marks, names):
                vo.wait_until(mk)
                self.play(FadeIn(n_), GrowFromCenter(mk_[0]), FadeIn(mk_[1]), FadeIn(mk_[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
