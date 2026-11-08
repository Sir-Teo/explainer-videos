from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Values(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Learning values", r"Can a machine learn what we want by watching what we do?", lit=(2000, 2018), part=PART)
        with self.voiceover("Chapter three. Learning values."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.irl()
        self.nfl()
        self.hume()
        self.practice()

    def irl(self):
        head = history_card(2000, r"Ng and Russell", r"``Algorithms for Inverse Reinforcement Learning''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"inverse RL", r"observe behaviour, \ infer the reward it maximizes", TRUEV),
                (r"the degeneracy", r"a reward of zero everywhere makes every behaviour optimal: \ Ng and Russell saw it at once", RISK),
                (r"Boltzmann rationality", r"assume people choose better options more often: \ $P(a) \propto e^{\beta R(a)}$", HUMAN),
                (r"from comparisons", r"Christiano et al. \ (2017): \ learn a reward from people's choices between two behaviours", PROXYC)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "If we cannot write down what we want, perhaps the machine can learn it by watching us. <bookmark "
            "mark='a'/>Andrew Ng and Stuart Russell posed inverse reinforcement learning in 2000: given an agent's "
            "behaviour, infer the reward it is maximizing. <bookmark mark='b'/>They saw a problem at once. A reward "
            "of zero everywhere makes every behaviour optimal, so it explains anything. <bookmark mark='c'/>The usual "
            "remedy is a model of human rationality: Boltzmann rationality assumes people choose better options more "
            "often, with probability proportional to e to the beta times the reward, where beta measures how rational "
            "they are. <bookmark mark='d'/>Paul Christiano and colleagues learned rewards from people's comparisons "
            "between two behaviours, the method behind training language models from human feedback. Each method "
            "needs an assumption about how values turn into choices."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def nfl(self):
        d = load("nfl")
        opts, pol, pairs = d["options"], d["policy"], d["pairs"]
        assert all(p0["error"] < 1e-12 for p0 in pairs)
        assert [p0["best"] for p0 in pairs] == ["tea", "tea", "water", None]
        head = label(r"No free lunch for preferences \ (Armstrong and Mindermann, \ 2018)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        # the observed behaviour as bars
        bars = VGroup()
        for i, (o, p) in enumerate(zip(opts, pol)):
            x = -5.6 + i * 0.95
            r = Rectangle(width=0.6, height=p * 3.2, fill_color=HUMAN, fill_opacity=0.8, stroke_width=0).move_to(
                [x, 1.05 + p * 1.6, 0])
            bars.add(VGroup(r, label(f"{p:.2f}", font_size=16, color=HUMAN).next_to(r, UP, buff=0.06),
                            label(o, font_size=16, color=GREY_A).move_to([x, 0.8, 0])))
        btitle = label(r"what she chooses, \ and how often", font_size=19, color=HUMAN).move_to([-4.2, 3.0, 0])
        hd = [r"\text{planner}", r"\text{reward: tea, coffee, water, juice}", r"\text{predicted choices}",
              r"\text{best by her lights}"]
        cells = []
        names = {"rational": (r"rational, \ $\beta = 1$", TRUEV), "twice as rational": (r"twice as rational", TRUEV),
                 "anti-rational": (r"anti-rational, \ $\beta = -1$", RISK), "indifferent": (r"indifferent", PROXYC)}
        for p0 in pairs:
            nm, col = names[p0["planner"]]
            cells.append([label(nm, font_size=17, color=col),
                          label(", \\ ".join(f"{(r if abs(r) > 1e-9 else 0.0):.2f}" for r in p0["reward"]), font_size=17),
                          label(", \\ ".join(f"{x:.2f}" for x in p0["predicted"]), font_size=17, color=HUMAN),
                          label(p0["best"] or r"none", font_size=17, color=GOAL)])
        grid = ValueGrid(hd, cells, col_w=[3.0, 4.2, 3.4, 2.4], cell_h=0.55, font_size=16).move_to([0, -1.75, 0])
        with self.voiceover(
            "Stuart Armstrong and Sören Mindermann turned the problem into a theorem. The Reasoner shows its core "
            "on a small case. <bookmark mark='a'/>A person chooses among four drinks: tea half the time, coffee "
            "thirty percent, juice fifteen, water five. What does she value? <bookmark mark='b'/>If she is "
            "Boltzmann-rational, her reward is the logarithm of how often she chooses: tea highest. <bookmark "
            "mark='c'/>If she is twice as rational, the rewards are halved; the same choices follow exactly. "
            "<bookmark mark='d'/>If she is anti-rational, systematically choosing what she likes least, her reward "
            "is the negative: she values water most, and the predicted choices are again exactly the same. "
            "<bookmark mark='e'/>And if her choices ignore her values altogether, any reward will do, even zero. "
            "Every row predicts her behaviour perfectly. <bookmark mark='f'/>Armstrong and Mindermann proved that "
            "this holds in general: behaviour can be decomposed into a planner and a reward in many ways, and a "
            "preference for simple explanations favours the degenerate ones, like the indifferent planner. What she "
            "values cannot be read off what she does without an assumption about how well she acts on it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(btitle), LaggedStart(*[FadeIn(b0) for b0 in bars], lag_ratio=0.2))
            self.play(FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("bcde", range(4)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c0) for c0 in grid.cell[r]])
            vo.wait_until("f")
            self.play(Indicate(grid.column(2), color=HUMAN, scale_factor=1.04),
                      Indicate(grid.column(3), color=GOAL, scale_factor=1.08))
        self.clear_scene()

    def hume(self):
        head = label(r"Hume's law, \ as a theorem about learning", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Part 37", r"no `ought' follows from premises that are only `is': \ Hume; \ Schurz's theorem", HUMAN),
                (r"here", r"no reward follows from behaviour alone: \ the planner must be assumed", TRUEV),
                (r"the escape", r"normative assumptions: \ about human rationality, \ biases and error", PROXYC),
                (r"so", r"value learning needs a theory of human error: \ psychology and philosophy, \ not more data", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "This is an old wall in a new place. <bookmark mark='a'/>Part 37 met Hume's law, that no ought follows "
            "from premises that state only what is, and Gerhard Schurz's theorem that makes it precise. <bookmark "
            "mark='b'/>Armstrong and Mindermann's result is Hume's law for machines that learn: no reward follows "
            "from behaviour alone, because the same behaviour fits many pairs of a planner and a reward. <bookmark "
            "mark='c'/>The escape is the same as Hume's: add bridge principles. Here they are normative assumptions "
            "about human rationality: that people mostly act on their values, that certain mistakes are biases, that "
            "regret reveals error. <bookmark mark='d'/>So value learning cannot be finished by more data. It needs a "
            "theory of when people act well and when they err, which is a question for psychology and for philosophy. "
            "This is the first half of the last brick in the Wall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def practice(self):
        head = label(r"Learning from feedback, \ in practice", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"RLHF", r"Ouyang et al. \ (2022): \ a reward model fitted to human comparisons, \ then a policy optimized against it", TRUEV),
                (r"Part 39", r"the fitted reward aggregates disagreeing raters like a Borda count \ (Siththaranjan et al., \ 2023)", HUMAN),
                (r"Constitutional AI", r"Bai et al. \ (2022): \ feedback from a model guided by written principles", PROXYC),
                (r"direct preference optimization", r"Rafailov et al. \ (2023): \ skip the reward model; \ the same Bradley--Terry assumption inside", ROBOT)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Modern assistants are trained this way. <bookmark mark='a'/>Long Ouyang and colleagues fitted a reward "
            "model to human comparisons between answers, then optimized the language model against it: reinforcement "
            "learning from human feedback. <bookmark mark='b'/>Part 39 showed what that fit does when raters "
            "disagree: it aggregates them like a Borda count, which can pass over the answer a majority prefers. "
            "<bookmark mark='c'/>Yuntao Bai and colleagues replaced much of the human feedback with feedback from a "
            "model guided by a written list of principles: a constitution. <bookmark mark='d'/>Rafael Rafailov and "
            "colleagues showed how to skip the reward model altogether, though the same Bradley and Terry assumption "
            "about noisy rational choice sits inside. Every method makes some assumption about how values become "
            "choices; the theorem says one must."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
