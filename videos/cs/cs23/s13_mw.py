from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Weights(VoiceoverScene):
    def construct(self):
        self.card()
        self.experts()
        self.proof()
        self.games()

    def card(self):
        card = chapter_card(12, r"Multiplicative weights", r"How do you learn from experts you can't trust?",
                            lit=(1994, 2012), extra=((1994, r"Littlestone--Warmuth"), (2012, r"Arora--Hazan--Kale")),
                            part=PART)
        with self.voiceover("Chapter twelve. Multiplicative weights."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def experts(self):
        m = load("mw")
        W = np.array(m["weights"])
        n = m["n"]
        head = label(r"Following the experts", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, len(W), len(W) // 5], y_range=[0, 1, 0.25], x_length=6.0, y_length=2.5,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.8).shift(UP * 1.25)
        curves = VGroup()
        for j in range(n):
            col = YES if j == m["best"] else GREY_C
            curves.add(ax.plot_line_graph(list(range(len(W))), W[:, j].tolist(), line_color=col, add_vertex_dots=False,
                                          stroke_width=3 if j == m["best"] else 1.5))
        cap = label(r"weights of 10 experts over 3,000 rounds; \\ the green one is wrong 45\% of the time, \ the others "
                    r"50\%", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        rows = [[words(r["T"]), f"{r['regret']:.0f}", f"{r['bound']:.0f}"] for r in m["rows"]]
        tab = grid_table([r"rounds $T$", r"regret", r"$\sqrt{(T \ln n)/2}$"], rows, widths=[1.8, 1.4, 2.4], row_h=0.32,
                         font_size=19, mono_cols=(), colors=[[WHITE, HEAD, GREY_A]] * len(rows))
        tab.next_to(cap, DOWN, buff=0.25).align_to(ax, LEFT)
        side = VGroup(
            label('each round: \\ a distribution over experts; \\\\ compute expected loss, \\ no realized expert draw', font_size=21, color=WHITE),
            MathTex(r"w_i \leftarrow w_i \, e^{-\eta\, \ell_i}", font_size=34, color=LAM),
            label(r"multiply the weight of each expert who erred", font_size=21, color=LAM),
            label('\\textbf{expected-loss regret}: \\ against the best fixed expert in hindsight', font_size=21,
                  color=HEAD),
            MathTex(r"\text{regret} \le \sqrt{\tfrac{T}{2} \ln n}", font_size=32, color=YES),
            label('losses in $[0,1]$; \\ eta retuned for each displayed $T$; \\\\ realized sampled loss needs a separate deviation bound', font_size=21,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            (
            "Multiplicative weights turns past losses into a distribution over experts. <bookmark mark='a'/> "
            "Each round our calculation assigns a probability to every expert before seeing that round's losses; "
            "it accumulates the distribution's expected loss, without sampling a realized expert. <bookmark "
            "mark='b'/> Multiply weights by the exponential of minus eta times loss, computed in stable log "
            "space. <bookmark mark='c'/> These seeded binary losses give one expert error probability forty-five "
            "percent and the rest fifty percent. Their finite histories are retained. <bookmark mark='d'/> "
            'Expected-loss regret compares the algorithm with the best fixed expert in hindsight. <bookmark '
            "mark='e'/> For losses in zero to one, the bound is log n over eta plus eta T over eight. Choosing "
            "eta for each displayed horizon gives the square root of T log n over two. <bookmark mark='f'/> "
            "Independent prefix-loss softmax calculations reproduce every row. A sampled expert's realized loss "
            'would additionally require a probabilistic deviation statement.'
        )
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.05), FadeIn(cap), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]), FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()

    def proof(self):
        head = label(r"Why the bound holds: \ watch the total weight", font_size=32).to_edge(UP, buff=0.35)
        rows = VGroup(
            MathTex(r"W_t = \sum_i w_i(t), \qquad W_0 = n", font_size=34, color=WHITE),
            MathTex(r"W_T \;\ge\; w_{\text{best}}(T) \;=\; e^{-\eta L^*}", font_size=34, color=YES),
            MathTex(r"W_{t+1} \;\le\; W_t\, e^{-\eta \ell_t + \eta^2/8}", font_size=34, color=NO),
            MathTex(r"e^{-\eta L^*} \;\le\; n\, e^{-\eta L + \eta^2 T/8}", font_size=34, color=LAM),
            MathTex(r"L - L^* \;\le\; \frac{\ln n}{\eta} + \frac{\eta T}{8} \;=\; \sqrt{\tfrac{T}{2}\ln n} \quad "
                    r"\text{at } \eta = \sqrt{8 \ln n / T}", font_size=34, color=HEAD),
        ).arrange(DOWN, buff=0.36).next_to(head, DOWN, buff=0.45).shift(LEFT * 2.2)
        notes = VGroup(
            label(r"start: \ every weight is 1", font_size=20, color=WHITE),
            label(r"the best expert's weight alone, \\ after its total loss $L^*$", font_size=20, color=YES),
            label(r"each round, \ the total shrinks by \\ about our expected loss $\ell_t$ \ (Hoeffding)", font_size=20,
                  color=NO),
            label(r"chain the rounds: \ $L = \sum_t \ell_t$", font_size=20, color=LAM),
            label(r"take logs, \ choose $\eta$", font_size=20, color=HEAD),
        )
        for n_, r_ in zip(notes, rows):
            n_.next_to(rows, RIGHT, buff=0.6).align_to(n_, LEFT).set_y(r_.get_y())
        notes.align_to(rows.get_right() + RIGHT * 0.6, LEFT)
        if notes.get_right()[0] > 6.9:
            notes.shift(LEFT * (notes.get_right()[0] - 6.9))
        tail = label(r"a \textbf{potential} argument: \ the weight can't fall fast unless we lose, \ and can't fall below "
                     r"the best expert's", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The proof is four lines, and it is worth seeing once. <bookmark mark='a'/> Watch the total weight. It "
            "starts at n, one per expert. <bookmark mark='b'/> At the end it is at least the weight of the best "
            "expert alone, which has been multiplied by e to the minus eta once for each of its losses. <bookmark "
            "mark='c'/> And in each round, when we follow an expert in proportion to the weights, the total weight "
            "shrinks by a factor of about e to the minus eta times our expected loss that round, with a small "
            "correction from Hoeffding's inequality. <bookmark mark='d'/> Chain the rounds together, and the two "
            "facts squeeze: our loss cannot be much more than the best expert's, or the weight would have fallen "
            "below the best expert's own. <bookmark mark='e'/> Take logarithms, choose eta to balance the two terms, "
            "and the regret is the square root of T over two times log n. <bookmark mark='f'/> It is a potential "
            "argument, like the amortized analyses of Parts 16 and 17, and the same pattern proves boosting and the minimax "
            "theorem."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_, n_ in zip("abcde", rows, notes):
                vo.wait_until(mk)
                self.play(FadeIn(r_), FadeIn(n_))
            vo.wait_until("f")
            self.play(FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()

    def games(self):
        m = load("mw")
        head = label(r"One algorithm, \ many theorems", font_size=34).to_edge(UP, buff=0.35)
        rows = [[words(g["T"]), f"{g['lo']:.4f}", f"{g['hi']:.4f}", f"{g['hi'] - g['lo']:.4f}"] for g in m["game"]]
        tab = grid_table([r"rounds", r"row player guarantees", r"column player concedes", r"gap"], rows,
                         widths=[1.6, 3.6, 3.8, 1.6], row_h=0.42, font_size=21, mono_cols=(),
                         colors=[[WHITE, YES, NO, HEAD]] * len(rows))
        lines = VGroup(
            label(r"\textbf{zero-sum games}: \ one player runs multiplicative weights, \ the other best-responds", font_size=22,
                  color=WHITE),
            label(rf"finite empirical lower/upper bounds; \ exact rational equilibrium value {m['game_value']:.4f}", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.4)
        tab.next_to(lines, DOWN, buff=0.35).set_x(0)
        more = VGroup(
            label(r"\textbf{boosting} \ (AdaBoost, \ Freund and Schapire, 1995): \ weights on examples, \ not experts \ "
                  r"(\textit{AI, Built} Part 6)", font_size=21, color=LAM),
            label(r"\textbf{approximate LP}: \ weights on constraints; \ Plotkin, \ Shmoys and Tardos; \ fast approximate "
                  r"max flow", font_size=21, color=HEAD),
            label(r"Arora, \ Hazan and Kale (2012): \ ``a meta-algorithm and its applications''", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            (
            "The same update supplies finite game certificates. <bookmark mark='a'/> Let the maximizing row "
            'player use multiplicative weights and the column player choose a best response each round. '
            "<bookmark mark='b'/> Average the actual row and column distributions. The smallest payoff against "
            'the averaged row is a lower bound on the game value; the largest against the averaged column is an '
            'upper bound. Both distributions are retained and checked. A separate exact rational equilibrium '
            "certifies this game's value near zero point four eight four six. Finite gaps are not exact "
            "convergence. <bookmark mark='c'/> Related weighting ideas power boosting, with its own assumptions "
            "and update rules. <bookmark mark='d'/> Constraint weights also support approximate packing and flow "
            "solvers with explicit width and accuracy parameters. <bookmark mark='e'/> Arora, Hazan and Kale "
            'survey this shared potential-method pattern and its applications.'
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(lines[1]))
            for mk, n_ in zip("cde", more):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
