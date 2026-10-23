from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import PART, PRM_C, RIGHT_C, SEARCH, WRONG_C, chip, load


def build_tree(levels, truth_steps):
    """Nested dict for SearchTree from the beam search's levels: a node per candidate partial chain; only the kept
    ones have children."""
    root = {"children": [], "color": GREY_B, "val": None}
    nodes = {(): root}
    for lev in levels:
        for steps, score, kept in lev:
            parent = nodes.get(tuple(steps[:-1]))
            if parent is None:
                continue
            j = len(steps) - 1
            ok = j < len(truth_steps) and steps[-1] == truth_steps[j]
            n = {"children": [], "val": int(steps[-1]), "score": float(score), "kept": bool(kept),
                 "color": (RIGHT_C if ok else WRONG_C) if kept else GREY_D, "ok": ok}
            parent["children"].append(n)
            if kept:
                nodes[tuple(steps)] = n
    return root


class Search(VoiceoverScene):
    def construct(self):
        self.card()
        self.analogy()
        self.history()
        self.tree()
        self.compare()

    # ------------------------------------------------------------------
    def analogy(self):
        rows = [
            (r"a position", r"a partial chain of thought"),
            (r"a move", r"the next step of thought"),
            (r"the policy network's prior", r"the model's probability of each next step"),
            (r"the value network", r"a process reward model"),
            (r"win or lose", r"the checker: \ right or wrong"),
        ]
        h = VGroup(label(r"Part 26: \ AlphaZero", font_size=28, color=GREY_A),
                   label(r"Part 28: \ search over thoughts", font_size=28, color=SEARCH))
        h[0].move_to([-3.3, 2.6, 0])
        h[1].move_to([3.3, 2.6, 0])
        tab = VGroup()
        for i, (a, b) in enumerate(rows):
            y = 1.6 - i * 0.85
            tab.add(VGroup(label(a, font_size=26, color=GREY_B).move_to([-3.3, y, 0]),
                           MathTex(r"\longleftrightarrow", font_size=34, color=GREY_D).move_to([0, y, 0]),
                           label(b, font_size=26, color=WHITE).move_to([3.3, y, 0])))
        line = Line([0, 3.0, 0], [0, -2.6, 0], color=GREY_D, stroke_width=1).set_opacity(0)
        diff = label(r"the difference: \ a board offers at most a few hundred moves; \ a step of thought, \ a "
                     r"vocabulary at every token",
                     font_size=24, color=C.SURPRISE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Search is how Part 26's game players thought ahead, and the parts carry over almost one for one. "
            "<bookmark mark='a'/> A position becomes a partial chain of thought; a move, the next step. "
            "<bookmark mark='b'/> AlphaZero's policy network, its sense of which moves are worth trying, becomes the "
            "language model's own probabilities for the next step. <bookmark mark='c'/> The value network, how good a "
            "position looks, becomes a process reward model. <bookmark mark='d'/> And winning or losing becomes the "
            "checker. <bookmark mark='e'/> The difference is the size of the tree: a board offers at most a few hundred "
            "legal moves, a language model a whole vocabulary at every token, and a step of thought is many tokens "
            "long."
        ) as vo:
            self.play(FadeIn(h), FadeIn(line))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
            vo.wait_until("d")
            self.play(FadeIn(tab[4]))
            vo.wait_until("e")
            self.play(FadeIn(diff))
        self.wait(0.3)
        self.clear_scene()

    def card(self):
        card = chapter_card(11, r"Searching over thoughts", r"Can we search for a good chain, instead of sampling one?",
                            lit=(2023, 2025), part=PART)
        with self.voiceover("Chapter eleven. Searching over thoughts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(2023, r"S.~Yao et al., \ Princeton and Google DeepMind: \ \textit{Tree of Thoughts}",
                         r"the model proposes several next thoughts and judges them; \ search keeps the promising ones. "
                         r"\ Game of 24 with GPT-4: \ $4\%$ with a chain of thought, \ $74\%$ with the tree",
                         width=6.4, color=SEARCH),
            history_card(2025, r"X.~Guan et al., \ Microsoft: \ \textit{rStar-Math}", r"Monte Carlo tree search over "
                         r"steps, \ guided by a learned process model: \ a $7$B model from $58.8\%$ to $90.0\%$ on MATH",
                         width=6.4, color=PRM_C),
            history_card(2024, r"AlphaProof \ (Part 26's AlphaZero, \ in Lean)", r"search over proof steps, \ every "
                         r"step checked by a proof assistant", width=6.4, color=C.INTERVAL),
            history_card(2025, r"DeepSeek-R1: \ MCTS, \ ``unsuccessful''", r"tokens make the tree enormous, \ and the "
                         r"value model that guides it is hard to train", width=6.4, color=WRONG_C),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3)).move_to(DOWN * 0.1)
        # schematic: whole chains judged at the end, against a tree judged step by step
        rows_ = VGroup(*[VGroup(*[RoundedRectangle(width=0.42, height=0.32, corner_radius=0.05, stroke_width=1.5,
                                                    stroke_color=GREY_B, fill_color=GREY_B, fill_opacity=0.2)
                                  for _ in range(5)]).arrange(RIGHT, buff=0.08) for _ in range(4)]).arrange(DOWN, buff=0.22)
        ends = VGroup(*[Text("?", font_size=24, color=C.BITS).next_to(r_, RIGHT, buff=0.2) for r_ in rows_])
        whole = VGroup(rows_, ends).move_to([-3.4, -0.1, 0])
        wl = label(r"sampling and voting: \\ whole chains, \ judged at the end", font_size=24, color=GREY_A)
        wl.next_to(whole, UP, buff=0.4)
        pts = {(0, 0): [3.4, 1.0]}
        for k_, x in enumerate((2.2, 3.4, 4.6)):
            pts[(1, k_)] = [x, 0.0]
        for k_, x in enumerate((1.8, 2.6, 4.2, 5.0)):
            pts[(2, k_)] = [x, -1.0]
        par_ = {(1, 0): (0, 0), (1, 1): (0, 0), (1, 2): (0, 0), (2, 0): (1, 0), (2, 1): (1, 0), (2, 2): (1, 2),
                (2, 3): (1, 2)}
        kept_ = {(0, 0), (1, 0), (1, 2), (2, 1), (2, 2)}
        edges_ = VGroup(*[Line(pts[par_[k_]] + [0], pts[k_] + [0], stroke_width=3 if k_ in kept_ else 1.2,
                               color=SEARCH if k_ in kept_ else GREY_D) for k_ in par_])
        dots_ = VGroup(*[Dot(pts[k_] + [0], radius=0.1, color=SEARCH if k_ in kept_ else GREY_D) for k_ in pts])
        stepw = VGroup(edges_, dots_)
        sl_ = label(r"search: \\ judged at every step, \ the best kept", font_size=24, color=SEARCH)
        sl_.next_to(stepw, UP, buff=0.4).align_to(wl, UP)
        sch_ = note(r"schematic").to_corner(DR, buff=0.3)
        intro = VGroup(whole, wl, stepw, sl_, sch_)
        with self.voiceover(
            "Sampling chains and voting treats each chain as a whole. Search works step by step: propose several next "
            "thoughts, judge them, and keep going from the most promising. <bookmark mark='a'/> In 2023, Tree of Thoughts let GPT-4 propose and judge its own next thoughts; on a "
            "puzzle, making 24 from four numbers, it went from 4 percent with a chain of thought to 74. "
            "<bookmark mark='b'/> In 2025, Microsoft's rStar-Math ran Monte Carlo tree search over steps, guided by a "
            "learned process model, and took a seven-billion-parameter model from 59 to 90 percent on competition "
            "maths. <bookmark mark='c'/> AlphaProof searched over steps of formal proofs, every step checked by a "
            "machine; we'll meet it in chapter thirteen. <bookmark mark='d'/> But DeepSeek tried tree search for "
            "R1 and gave up: over tokens the tree is enormous, and the value model that should guide it is hard to "
            "train. At the frontier, search mostly survives as sampling many chains in parallel."
        ) as vo:
            self.play(FadeIn(whole), FadeIn(wl), FadeIn(sch_))
            self.play(FadeIn(sl_), Create(edges_), FadeIn(dots_), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(intro))
            for k, mk in enumerate("abcd"):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tree(self):
        s = load("think_search")
        d = np.asarray(s["tree_d"])
        digits = [int(x) for x in d if x < 10]
        truth = list(np.cumsum(digits))
        levels = [[(list(map(int, st)), float(sc), bool(k)) for st, sc, k in lev] for lev in s["tree"]]
        best = [int(x) for x in s["tree_best"]]
        root = build_tree(levels, truth)
        t = SearchTree(root, width=12.6, level_height=0.58, radius=0.09, center=[0, -0.4, 0],
                       edge_width=lambda nd: 3.0 if nd.get("kept") else 1.0)
        q = VGroup(*[chip(str(x), 0.4, GREY_B, 20) for x in digits]).arrange(RIGHT, buff=0.06).to_edge(UP, buff=0.3)
        ql = label(rf"a {len(digits)}-digit list: \ search over the running totals", font_size=22, color=GREY_A)
        ql.next_to(q, LEFT, buff=0.3)
        keep_in_frame(VGroup(ql, q))
        key = VGroup(label(r"kept, \ right", font_size=18, color=RIGHT_C), label(r"kept, \ wrong", font_size=18,
                                                                                 color=WRONG_C),
                     label(r"pruned by the process grader", font_size=18, color=GREY_C)).arrange(RIGHT, buff=0.5)
        key.to_corner(DL, buff=0.3)
        by_level = {}
        for i in range(1, len(t.nodes)):
            by_level.setdefault(t.level[i], []).append(i)
        ans_ok = best == truth[:len(best)]
        tag = note(rf"computed: \ beam $3$, \ $3$ proposals each; \\ the most branching search of "
                   rf"${int(s['tree_of'])}$ lists").to_corner(DR, buff=0.2)
        if ans_ok:
            fin = "At the end, the best surviving chain is right all the way down."
        else:
            fin = "At the end the best surviving chain still has a wrong step: a grader can be fooled."
        with self.voiceover(
            "Here is search on our adding model. At each step, every surviving partial chain proposes three next "
            "running totals; the process grader of chapter three scores every candidate; the best three survive. "
            "<bookmark mark='a'/> Green nodes are right totals, red are wrong ones that survived, grey were pruned. "
            f"<bookmark mark='b'/> {fin}"
        ) as vo:
            self.play(FadeIn(q), FadeIn(ql), FadeIn(key), FadeIn(tag), FadeIn(t.nodes[0]))
            vo.wait_until("a")
            K = max(by_level)
            dt = max(0.3, min(1.0, (vo.until("b") - 0.3) / max(K, 1)))
            for lv in range(1, K + 1):
                ids = by_level[lv]
                self.play(*[Create(t.edges[i]) for i in ids], *[FadeIn(t.nodes[i]) for i in ids], run_time=dt)
            vo.wait_until("b")
            path = [i for i in range(1, len(t.nodes)) if t.node_data[i].get("kept")]
            self.play(Indicate(VGroup(*[t.nodes[i] for i in path]), color=SEARCH, scale_factor=1.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        s = load("think_search")
        W = np.asarray(s["beam_width"])
        ba = np.asarray(s["beam_acc"])
        bN, bo = np.asarray(s["bon_N"]), np.asarray(s["bon_acc"])
        order = np.argsort(W)
        W, ba = W[order], ba[order]
        lw, lN = np.log2(W), np.log2(bN)
        xmax = float(max(lw.max(), lN.max()))
        lo = float(np.floor(min(ba.min(), bo.min()) * 10) / 10)
        g = axes([0, xmax], [lo, 1.0], x_length=7.0, y_length=4.2, xlabel=r"samples per step \ (the same budget of "
                 r"tokens)", ylabel=rf"right, \ ${int(s['n'])}$-digit lists", xticks=list(lN), xfmt=lambda x: f"{int(2 ** x)}",
                 yticks=[lo, 1.0], yfmt=lambda v: rf"{int(round(100 * v))}\%", center=[-1.4, -0.3, 0])
        cb = curve(g.ax, lw, ba, SEARCH, 4)
        co = curve(g.ax, lN, bo, PRM_C, 4)
        db = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.05, color=SEARCH) for x, y in zip(lw, ba)])
        do = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.05, color=PRM_C) for x, y in zip(lN, bo)])
        lg = legend([(SEARCH, r"beam search, \ step by step"), (PRM_C, r"best-of-$N$ whole chains")], font_size=20)
        lg.next_to(g, RIGHT, buff=0.3).shift(UP * 0.8)
        tag = note(rf"computed: \ ${int(s['nq'])}$ lists; \ both use the same process grader").to_corner(DR, buff=0.2)
        diff = float(np.mean(np.interp(lN, lw, ba) - bo))
        if diff > 0.02:
            said = ("At every budget, searching step by step beats choosing among whole chains: it catches a wrong "
                    "total the moment it is written, instead of hoping one whole chain avoided every slip.")
        elif diff < -0.02:
            said = ("Here, choosing among whole chains does better than searching step by step: the grader's mistakes "
                    "at each step compound, and pruning early throws away chains that would have recovered.")
        else:
            said = "Here the two end up close: on a problem this regular, a good grader helps either way."
        both_fall = ba[-1] < ba.max() - 0.05 and bo[-1] < bo.max() - 0.05
        if both_fall:
            trend = (f"But both get worse as they widen: beam search falls from {100 * ba.max():.0f} to "
                     f"{100 * ba[-1]:.0f} percent, best-of-N from {100 * bo.max():.0f} to {100 * bo[-1]:.0f}. The "
                     "wider the search, the more it finds of what fools the grader, chapter three's lesson again. A "
                     "search is only as good as its judge.")
        else:
            trend = (f"At the widest, beam search reaches {100 * ba[-1]:.0f} percent and best-of-N "
                     f"{100 * bo[-1]:.0f}.")
        ends = VGroup(Dot(g.ax.c2p(lw[-1], ba[-1]), radius=0.1, color=SEARCH),
                      Dot(g.ax.c2p(lN[-1], bo[-1]), radius=0.1, color=PRM_C))
        with self.voiceover(
            "Is search worth it? Compare it with best-of-N, using the same grader and the same number of tokens. "
            "<bookmark mark='a'/> Best-of-N samples N whole chains and keeps the one the grader likes best. "
            f"<bookmark mark='b'/> Beam search spends the same tokens step by step. <bookmark mark='c'/> {said} "
            f"<bookmark mark='d'/> {trend}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(co), FadeIn(do), FadeIn(lg[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cb), FadeIn(db), FadeIn(lg[0]), run_time=1.5)
            vo.wait_until("d")
            self.play(Flash(ends[0], color=SEARCH), Flash(ends[1], color=PRM_C), FadeIn(ends))
        self.wait(0.3)
        self.clear_scene()
