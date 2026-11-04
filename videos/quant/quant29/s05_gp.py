from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import FORMULA, GP_C, HURDLE, PART, RAND_C, TRAIN_C, VALID_C, fit_right, illustration, load, tt


def node(text, col, fs=20):
    t = label(text, font_size=fs, color=col)
    box = RoundedRectangle(width=max(t.width + 0.35, 1.0), height=0.52, corner_radius=0.1, stroke_color=col,
                           fill_color=col, fill_opacity=0.12)
    t.move_to(box)
    return VGroup(box, t)


def small_tree(spec, origin, dx=1.3, dy=0.85):
    """spec: (text, colour, [children]); returns (group, {path: node}) laid out top-down from ``origin``."""
    nodes, edges = {}, VGroup()

    def width(s):
        return max(1, sum(width(c) for c in s[2])) if s[2] else 1

    def place(s, x, y, path):
        n = node(s[0], s[1]).move_to([x, y, 0])
        nodes[path] = n
        w = width(s)
        cx = x - dx * (w - 1) / 2
        for i, c in enumerate(s[2]):
            wc = width(c)
            px = cx + dx * (wc - 1) / 2
            ch = place(c, px, y - dy, path + (i,))
            edges.add(Line(n.get_bottom(), ch.get_top(), color=GREY_C, stroke_width=2))
            cx += dx * wc
        return n
    place(spec, origin[0], origin[1], ())
    return VGroup(edges, *nodes.values()), nodes


class GP(VoiceoverScene):
    def construct(self):
        g = load("gp")
        self.card()
        self.crossover()
        self.algorithm()
        self.runs(g)
        self.budget(g, load("random"))
        self.bloat(g)
        self.winners(g)
        self.allen()
        self.question()

    def card(self):
        c = chapter_card(4, r"Genetic programming", r"Can formulas be bred, the way a farmer breeds wheat?", part=PART)
        with self.voiceover("Chapter four. Random search wastes its draws: it never learns from a good formula. John Koza's "
                            "genetic programming, in 1992, bred programs instead. Can formulas be bred, the way a farmer "
                            "breeds wheat?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def crossover(self):
        A_ = (r"\texttt{rank}", GP_C, [(r"\texttt{sub}", GP_C, [(r"\texttt{close}", FORMULA, []),
                                                               (r"\texttt{ts\_mean}($\cdot$, 5)", QC.OPTION,
                                                                [(r"\texttt{close}", FORMULA, [])])])])
        B_ = (r"\texttt{neg}", GP_C, [(r"\texttt{mul}", GP_C, [(r"\texttt{delta}($\cdot$, 1)", QC.OPTION,
                                                               [(r"\texttt{volume}", FORMULA, [])]),
                                                              (r"\texttt{ret}", FORMULA, [])])])
        ta, na = small_tree(A_, (-3.6, 2.4))
        tb, nb = small_tree(B_, (3.6, 2.4))
        pa = label(r"parent A", font_size=20, color=GREY_B).next_to(ta, UP, buff=0.2)
        pb = label(r"parent B", font_size=20, color=GREY_B).next_to(tb, UP, buff=0.2)
        cut_a = SurroundingRectangle(VGroup(na[(0, 1)], na[(0, 1, 0)]), color=HURDLE, buff=0.08)
        cut_b = SurroundingRectangle(VGroup(nb[(0, 0)], nb[(0, 0, 0)]), color=HURDLE, buff=0.08)
        C_ = (r"\texttt{rank}", GP_C, [(r"\texttt{sub}", GP_C, [(r"\texttt{close}", FORMULA, []),
                                                               (r"\texttt{delta}($\cdot$, 1)", QC.OPTION,
                                                                [(r"\texttt{volume}", FORMULA, [])])])])
        tc, nc = small_tree(C_, (0, -0.6))
        ch = label(r"the child: A with B's subtree spliced in", font_size=20, color=HURDLE).next_to(tc, DOWN, buff=0.25)
        mut = wrapped_label(r"mutation: replace a random subtree with a fresh random one", 5.0, 17, GREY_A
                            ).to_corner(DR, buff=0.5).shift(UP * 0.4)
        with self.voiceover(
            "Two formulas that scored well are parents. <bookmark mark='a'/> Pick a random branch in each. "
            "<bookmark mark='b'/> The child is parent A with parent B's branch spliced in: closing price minus "
            "yesterday's change in volume, ranked. Nothing guarantees the child makes sense; selection decides. "
            "<bookmark mark='c'/> And now and then a mutation replaces a branch with a fresh random one, so the "
            "population does not run out of new material."
        ) as vo:
            self.play(FadeIn(ta), FadeIn(tb), FadeIn(pa), FadeIn(pb), FadeIn(illustration()))
            vo.wait_until("a")
            self.play(Create(cut_a), Create(cut_b))
            vo.wait_until("b")
            self.play(TransformFromCopy(VGroup(nb[(0, 0)], nb[(0, 0, 0)]), VGroup(nc[(0, 1)], nc[(0, 1, 0)])),
                      FadeIn(VGroup(tc[0], nc[()], nc[(0,)], nc[(0, 0)])), FadeIn(ch), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(mut))
        self.wait(0.4)
        self.clear_scene()

    def algorithm(self):
        rows = [cmath(r"\text{fitness}(f)", r"=", r"|\overline{IC}_{\text{train}}(f)| - \lambda\cdot\text{size}(f)", font_size=32,
                      colors={r"\text{fitness}(f)": GP_C}),
                cmath(r"\text{select}", r":", r"\text{the fittest of 5 drawn at random (a tournament)}", font_size=30),
                cmath(r"\text{breed}", r":", r"70\%\ \text{crossover},\ 20\%\ \text{mutation},\ 10\%\ \text{copied}", font_size=30),
                cmath(r"\text{repeat}", r":", r"100\ \text{formulas} \times 25\ \text{generations}, \text{ the best always kept}",
                      font_size=30)]
        whys = [why(r"the training score, minus a parsimony penalty $\lambda = 0.0005$ per node against bloat"),
                why(r"tournaments keep the pressure moderate: a mediocre formula sometimes wins its draw"),
                why(r"children are built from the parents' branches"),
                why(r"elitism: the champion survives unchanged into the next generation")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The algorithm in four lines. <bookmark mark='a'/> Fitness is the training score, minus a small penalty for "
            "every node. <bookmark mark='b'/> Parents are chosen by tournament: draw five at random, take the fittest. "
            "<bookmark mark='c'/> Children come from crossover most of the time, from mutation sometimes, and are "
            "copied otherwise. <bookmark mark='d'/> A population of a hundred, for twenty-five generations, and the best "
            "formula is always carried forward."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def runs(self, g):
        R = g["runs"]
        G = len(R[0])
        tr = np.array([[x["train"] for x in run] for run in R])
        va = np.array([[x["valid"] for x in run] for run in R])
        top = float(np.ceil(np.abs(tr).max() * 100 + 0.5) / 100)
        lo = float(np.floor(min(0.0, va.min()) * 100) / 100)
        gr = axes([0, G - 1], [lo, top], x_length=7.2, y_length=4.6, xlabel=r"generation", ylabel=r"the champion's IC",
                  xticks=[0, 10, 20], yticks=[lo, 0, top], font_size=15, yfmt=lambda v: f"{v:.2f}").move_to(
            LEFT * 1.8 + DOWN * 0.2)
        ax = gr.ax
        gens = np.arange(G)
        lt = VGroup(*[curve(ax, gens, np.abs(t), TRAIN_C, stroke_width=2.5) for t in tr])
        lv = VGroup(*[curve(ax, gens, v * np.sign(t), VALID_C, stroke_width=2.5) for t, v in zip(tr, va)])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(G - 1, 0), color=GREY_B, stroke_width=1.2)
        leg = legend([(TRAIN_C, r"on 2018--19, what it is bred for"), (VALID_C, r"on 2020, never seen")],
                     font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        ev = sum(run[-1]["evaluated"] for run in R)
        side = wrapped_label(rf"three runs from different random seeds; {ev:,} distinct formulas evaluated in all"
                             .replace(",", "{,}", 1), 3.4, 15, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        t_fin = np.abs(tr[:, -1])
        v_fin = va[:, -1] * np.sign(tr[:, -1])
        k_hi = int(np.argmax(t_fin))
        others = [k for k in range(len(R)) if k != k_hi]
        o_t = float(np.mean(t_fin[others]))
        o_v = float(np.mean(v_fin[others]))
        hi_t, hi_v = float(t_fin[k_hi]), float(v_fin[k_hi])
        ev_run = ev // len(R)
        with self.voiceover(
            "Three runs, from three random starts. <bookmark mark='a'/> On the training years, every champion improves "
            "or holds, generation by generation: evolution works on whatever it is rewarded for. <bookmark mark='b'/> On "
            "2020, which no generation saw, the runs split. The run that climbed highest, to a training score of "
            f"{hi_t:.3f}, fell furthest, to {hi_v:+.3f}. The other two stopped lower, at {o_t:.3f} on average, and kept "
            f"far more: {o_v:+.3f} in 2020. Each run also tried about {ev_run:,} formulas, and every one is a trial."
        ) as vo:
            self.play(FadeIn(gr), Create(zero), FadeIn(leg), FadeIn(side))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lt], run_time=2)
            vo.wait_until("b")
            self.play(*[Create(l_) for l_ in lv], run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def budget(self, g, r):
        b = r["best_by_n"]
        xr = np.log10([x["n"] for x in b])
        yr = [x["train"] for x in b]
        top = float(np.ceil(max(max(yr), max(abs(x["train"]) for run in g["runs"] for x in run)) * 100 + 1) / 100)
        gr = axes([1, 4], [0, top], x_length=7.2, y_length=4.4, xlabel=r"distinct formulas evaluated (log scale)",
                  ylabel=r"best training IC so far", xticks=[1, 2, 3, 4], yticks=[0, top / 2, top], font_size=15,
                  xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{v:.2f}").move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = gr.ax
        lr = curve(ax, xr, yr, RAND_C, stroke_width=3)
        lg = VGroup()
        for run in g["runs"]:
            ev = np.log10([max(x["evaluated"], 10) for x in run])
            lg.add(curve(ax, ev, [abs(x["train"]) for x in run], GP_C, stroke_width=2.5))
        leg = legend([(RAND_C, r"random search, Chapter 3"), (GP_C, r"genetic programming, three runs")], font_size=15
                     ).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        at1k = next(x for x in b if x["n"] == 1000)
        with self.voiceover(
            "Is evolution a better search than chance? Compare them at equal budgets. <bookmark mark='a'/> The grey line "
            "is random search: the best training score after each number of formulas tried, "
            f"{at1k['train']:.3f} by a thousand. <bookmark mark='b'/> The coloured lines are the three evolutionary runs, "
            "against the distinct formulas each had evaluated. Two of them keep pace with chance; the third climbs far "
            "above it. And that third run is the one whose edge vanished in 2020. A better optimiser of the training "
            "score is not a better finder of signals: past a point, it is a better finder of noise."
        ) as vo:
            self.play(FadeIn(gr), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lr), run_time=1.5)
            vo.wait_until("b")
            self.play(*[Create(l_) for l_ in lg], run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def bloat(self, g):
        R = g["runs"]
        G = len(R[0])
        ms = np.array([[x["mean_size"] for x in run] for run in R])
        bs = np.array([[x["size"] for x in run] for run in R])
        top = float(np.ceil(max(ms.max(), bs.max()) / 5) * 5)
        k_b = int(np.argmax([abs(run[-1]["train"]) for run in R]))      # the run that climbed highest
        gr = axes([0, G - 1], [0, top], x_length=7.2, y_length=4.4, xlabel=r"generation", ylabel=r"nodes in a formula",
                  xticks=[0, 10, 20], yticks=[0, top / 2, top], font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = gr.ax
        gens = np.arange(G)
        lm = VGroup(*[curve(ax, gens, m, GP_C, stroke_width=2.5) for m in ms])
        lb = VGroup(*[curve(ax, gens, b, HURDLE, stroke_width=2) for b in bs])
        leg = legend([(GP_C, r"the population's average"), (HURDLE, r"the champion")], font_size=15).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(r"bloat: branches that do nothing are copied along with the ones that work, because they "
                             r"protect the working parts from crossover; the parsimony penalty pushes back", 3.4, 15,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Genetic programs have a famous disease: bloat. <bookmark mark='a'/> In the run that climbed highest, the "
            f"average formula grew from {ms[k_b, 0]:.0f} nodes to {ms[k_b, -1]:.0f}, and its champion to "
            f"{bs[k_b, -1]:.0f}. In the other two, the penalty per node held the formulas short. <bookmark mark='b'/> "
            "Much of the growth is dead wood: branches that change little, carried along because they shield the "
            "working parts from being cut. And a bloated formula is harder to read, slower to run, and better at "
            "fitting noise."
        ) as vo:
            self.play(FadeIn(gr), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lm], *[Create(l_) for l_ in lb], run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def winners(self, g):
        k_hi = int(np.argmax([abs(run[-1]["train"]) for run in g["runs"]]))
        rows = VGroup()
        for k, run in enumerate(g["runs"]):
            last = run[-1]
            rows.add(VGroup(label(rf"run {k + 1}", font_size=20, color=GP_C),
                            label(tt(last["best"], 92), font_size=13, color=GREY_A),
                            MathTex(rf"{abs(last['train']):.3f}\ \to\ {last['valid'] * np.sign(last['train']):+.3f}",
                                    font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.12))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.2)
        if rows.width > 12.6:
            rows.scale_to_fit_width(12.6)
        foot = wrapped_label(r"each run's final champion, its IC on 2018--19 and then on 2020", 11.0, 16, GREY_B
                             ).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The three champions. <bookmark mark='a'/> Two of them can be read. One is a coin's lowest recent dollar "
            "volume, smoothed: how liquid it is, which on these coins is close to how big it is. The other is the "
            "average ratio of each day's low to its high: one minus the day's range, a measure of calm. Evolution "
            "rediscovered size and low volatility, the factors of Part twenty-four. <bookmark mark='b'/> The third, the "
            "one that fitted best, cannot be read, and its edge did not survive. A signal does not need a story to be "
            "real, but without one the only evidence is the out-of-sample number, and the count of formulas tried."
        ) as vo:
            self.play(FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Indicate(rows[k_hi], color=QC.LOSS, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def allen(self):
        card = firm_card(r"Allen and Karjalainen (1999)", r"`Using genetic algorithms to find technical trading rules', "
                         r"\textit{Journal of Financial Economics}: genetic programming bred market-timing rules for the "
                         r"S\&P 500 from daily prices, 1928--1995, each trained on one period, selected on the next, and "
                         r"tested on the years after",
                         numbers=((r"\times", r"after transaction costs, no consistent excess return over buying and "
                                               r"holding the index out of sample"),
                                  (r"\sigma\downarrow", r"the rules were in the market when daily volatility was low and "
                                                        r"out when it was high")),
                         source=r"JFE 51 (1999)", kind=r"Paper file", width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "This is not the first time evolution was set loose on a market. <bookmark mark='a'/> In 1999 Franklin Allen "
            "and Risto Karjalainen bred trading rules for the S&P 500 from nearly seventy years of daily prices, training each "
            "generation on one period, selecting on the next and testing on the years after. <bookmark mark='b'/> After "
            "costs, the rules did not beat simply holding the index. But what they had learned is telling: they stayed "
            "in the market when volatility was low and left when it was high. Evolution found calm then, too."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a GP run is scored on 2018--19 and its champion chosen by its 2020 score. Is 2020 still "
                       r"out of sample?")
        with self.voiceover(
            "Pause and predict. You run the evolution on 2018 and 2019, and then choose among the champions of many "
            "runs by their score on 2020. Is 2020 still out of sample?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
