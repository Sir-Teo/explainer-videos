from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import ALPHA27, PART, area_slivers, load


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        """Part 1 in eight pictures, each redrawn small from the part's own numbers."""
        lt, kl, od, sb = load("letters"), load("kl"), load("orders"), load("scoreboard")
        ty, ar, mi, z = load("typical"), load("arith"), load("mi"), load("lmzip")
        TW, TH = 3.0, 2.0

        def axes_box(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH - 0.2, tips=False,
                        axis_config={"stroke_color": GREY_D, "stroke_width": 1.5, "include_ticks": False})

        out = []
        # 1. the chain rule: nested slivers, from the coder's own steps
        g = VGroup()
        steps = ar["steps"][:3]
        for k, st in enumerate(steps):
            probs = np.asarray(st["probs"])
            idx = ALPHA27.index(st["symbol"])
            a, b = float(probs[:idx].sum()), float(probs[:idx + 1].sum())
            bar = Rectangle(width=TW, height=0.28, stroke_width=1, stroke_color=GREY_C, fill_color="#1B2638",
                            fill_opacity=1).move_to([0, 0.7 - 0.62 * k, 0])
            hi_ = Rectangle(width=max(TW * (b - a), 0.04), height=0.28, stroke_width=0, fill_color=C.INTERVAL,
                            fill_opacity=0.9).move_to(bar.get_left() + RIGHT * TW * (a + b) / 2)
            g.add(bar, hi_)
            if k < 2:
                g.add(Polygon(hi_.get_corner(DL), hi_.get_corner(DR), bar.get_corner(DR) + DOWN * 0.34,
                              bar.get_corner(DL) + DOWN * 0.34, stroke_width=0, fill_color=C.INTERVAL, fill_opacity=0.15))
        out.append((g, r"the chain rule", C.INTERVAL))
        # 2. entropy: the area picture
        g = area_slivers(lt["p"], W=TW, y0=-TH / 2 + 0.1, scale=0.15, order=list(lt["order"]), color=C.ENTROPY)
        out.append((g, rf"entropy: \ ${float(lt['H']):.2f}$ bits", C.ENTROPY))
        # 3. the typical set, at n = 100: a sliver of the sequences, most of the probability
        r100 = min(ty["rows"], key=lambda r: abs(r["n"] - 100))
        g = VGroup(Rectangle(width=TW, height=0.3, stroke_color=GREY_B, stroke_width=1).move_to(UP * 0.5),
                   Rectangle(width=TW, height=0.3, stroke_color=GREY_B, stroke_width=1).move_to(DOWN * 0.5))
        g.add(Rectangle(width=max(TW * 2 ** r100["log2_frac"], 0.03), height=0.3, stroke_width=0, fill_color=C.BITS,
                        fill_opacity=1).move_to(UP * 0.5).align_to(g[0], LEFT))
        g.add(Rectangle(width=TW * r100["P"], height=0.3, stroke_width=0, fill_color=C.BITS, fill_opacity=1)
              .move_to(DOWN * 0.5).align_to(g[1], LEFT))
        out.append((g, rf"typical: \ ${100 * r100['P']:.0f}\%$ of the probability", C.BITS))
        # 4. forward and reverse KL on two peaks
        x, pp = np.asarray(kl["x"]), np.asarray(kl["p"])
        fw, rv = np.asarray(kl["fwd"])[-1], np.asarray(kl["rev_a"])[-1]
        # Keep both complete Gaussian peaks on one common density scale.
        ymax = 1.15 * max(float(pp.max()), *(1 / (fit[1] * np.sqrt(2 * np.pi)) for fit in (fw, rv)))
        ax = axes_box([float(x[0]), float(x[-1]), 1], [0, ymax, 1])

        def gauss(m, s):
            return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))

        g = VGroup(ax, ax.plot_line_graph(x, pp, add_vertex_dots=False, line_color=C.TRUE_P, stroke_width=3),
                   ax.plot_line_graph(x, gauss(fw[0], fw[1]), add_vertex_dots=False,
                                      line_color=C.MODEL_Q, stroke_width=3),
                   ax.plot_line_graph(x, gauss(rv[0], rv[1]), add_vertex_dots=False,
                                      line_color=C.KL, stroke_width=3))
        out.append((g, r"forward and reverse $D_{\mathrm{KL}}$", C.KL))
        # 5. arithmetic coding: GPT-2 as a compressor
        nb = int(math.ceil(z["bits"] / 8))
        vals = [(z["bytes"], GREY_B), (z["compressors"]["xz"], C.COMPRESSOR), (nb, C.NEURAL)]
        g = VGroup(*[Rectangle(width=TW * v / vals[0][0], height=0.36, stroke_width=0, fill_color=c, fill_opacity=0.9)
                     .move_to([-TW / 2 + TW * v / vals[0][0] / 2, 0.55 - 0.55 * i, 0]) for i, (v, c) in enumerate(vals)])
        out.append((g, rf"GPT-2 as a compressor: \ ${nb}$ bytes", C.NEURAL))
        # 6. generalization: the books vs new text
        rows = od["rows"]
        ks = np.arange(len(rows))
        ax = axes_box([0, 14, 1], [0, 4.5, 1])
        g = VGroup(ax, ax.plot_line_graph(ks, [r["plugin"] for r in rows], add_vertex_dots=False, line_color=C.COUNTING,
                                          stroke_width=3),
                   ax.plot_line_graph(ks, [r["test"] for r in rows], add_vertex_dots=False, line_color=C.SURPRISE,
                                      stroke_width=3))
        out.append((g, r"memorizing $\ne$ generalizing", C.COUNTING))
        # 7. mutual information against distance: the long tail
        ds, mv = np.asarray(mi["d"], float), np.asarray(mi["mi"])
        ok = mv > 0
        ax = axes_box([0, 3, 1], [-6, 0, 1])
        g = VGroup(ax, ax.plot_line_graph(np.log10(ds[ok]), np.log10(mv[ok]), add_vertex_dots=False,
                                          line_color=C.CONTEXT, stroke_width=3))
        out.append((g, r"mutual information: \ a long tail", C.CONTEXT))
        # 8. the scoreboard
        vals = [r for r in sb["rows"] if r.get("bits") is not None]
        kind_col = {"count": C.COUNTING, "compressor": C.COMPRESSOR, "lm": C.NEURAL}
        g = VGroup()
        for k, r in enumerate(vals):
            wdt = TW * r["bits"] / 8.0
            g.add(Rectangle(width=wdt, height=0.11, stroke_width=0, fill_color=kind_col.get(r.get("kind"), GREY_B),
                            fill_opacity=0.9).move_to([-TW / 2 + wdt / 2, TH / 2 - 0.15 - k * 0.15, 0]))
        low = min(r["bits"] for r in vals)
        out.append((g, rf"$8 \to {low:.2f}$ bits", WHITE))
        tiles = Group()
        for pic, cap, col in out:
            box, c = tile_frame(cap, col)
            if c.width > box.width - 0.25:  # a long caption stays inside its frame
                c.scale_to_fit_width(box.width - 0.25)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, \ in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        z = load("lmzip")
        back = ("and decoded it back, letter for letter" if z["ok"] else
                "but its independent decoding failed, so that run is not a verified round trip")
        with self.voiceover(
            "Let's take stock. Guesses are probability distributions; the chain rule scores a whole text. Surprise "
            "had to be a logarithm, and entropy is the only consistent measure of uncertainty. Kraft's budget bounds "
            "uniquely decodable codes; Huffman is optimal for symbol codes, and long blocks can approach the entropy "
            "on average. A wrong "
            "model costs the cross-entropy. Arithmetic coding made predicting and compressing one thing, and GPT-2 "
            f"compressed a known-length prefix of our passage {back}. Counting taught generalization by failing at it, and mutual "
            "information showed how far back text remembers."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"the chain rule: \ next-token prediction", [13, 14, 28]),
            (r"cross-entropy: \ the training loss", [9, 11, 18]),
            (r"forward and reverse $D_{\mathrm{KL}}$", [20, 27]),
            (r"typical sets, \ and drawing from a model", [5]),
            (r"prediction $=$ compression", [12, 31]),
            (r"memorizing vs.\ generalizing", [7, 8]),
            (r"mutual information, \ long memory", [13, 15]),
            (r"softmax, \ and its logit derivative $q_k - [k = y]$", [4, 11]),
        ], font_size=24)
        with self.voiceover(
            "Almost everything here comes back. The chain rule is how language models generate text, and how "
            "reasoning models think out loud. Cross-entropy is the loss we'll minimize for the rest of the series. "
            "The divergence's two directions return in variational autoencoders and in alignment. Drawing typical "
            "text from a model is Part 5. And compression returns with scaling, and at the very end, when we ask "
            "what these models can be trusted with."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"From $H = -\sum_i p_i \log_2 p_i$, show the grouping rule: \ $H(p_1, p_2, p_3, \dots) = H(p_1 + p_2, p_3, "
            r"\dots) + (p_1 + p_2)\, H\big(\tfrac{p_1}{p_1 + p_2}, \tfrac{p_2}{p_1 + p_2}\big)$.",
            r"Can a prefix code have codeword lengths $1, 2, 3, 3, 3$? \ Can any uniquely decodable code?",
            r"Build a Huffman code for $(0.4, 0.2, 0.2, 0.1, 0.1)$. \ Find two optimal codes with different lengths, "
            r"and compare their average with $H$.",
            r"A coin lands heads with probability $0.1$; toss it $100$ times. \ About how many typical sequences are "
            r"there, and how likely is each, against the single likeliest sequence?",
            r"For $p = (\tfrac12, \tfrac12)$ and $q = (\tfrac14, \tfrac34)$, compute $D_{\mathrm{KL}}(p \,\|\, q)$ and "
            r"$D_{\mathrm{KL}}(q \,\|\, p)$.",
            r"Derive Laplace's rule $\frac{s+1}{n+2}$ from $\int_0^1 \theta^a (1 - \theta)^b\, d\theta = "
            r"\frac{a!\, b!}{(a + b + 1)!}$.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems to try, from the grouping rule to Laplace's rule of succession. Pause here and "
            "work through them; full solutions are in this part's notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 2, \ Thinking Machines", font_size=40).to_edge(UP, buff=0.4)
        # a search spreading over a grid from a start toward a goal: uniform (a disc) against guided (an ellipse)
        n, s = 17, 0.27
        start, goal = (8, 2), (8, 14)
        x0, y0 = -3.6, -0.3
        cells = VGroup(*[Square(s, stroke_width=0.6, stroke_color=GREY_D, fill_color="#141A24", fill_opacity=1)
                         .move_to([x0 + (j - n / 2 + 0.5) * s, y0 + (n / 2 - 0.5 - i) * s, 0])
                         for i in range(n) for j in range(n)])
        dist = np.array([[abs(i - start[0]) + abs(j - start[1]) for j in range(n)] for i in range(n)], float)
        h = np.array([[abs(i - goal[0]) + abs(j - goal[1]) for j in range(n)] for i in range(n)], float)
        st_ = Dot(cells[start[0] * n + start[1]].get_center(), radius=0.09, color=WHITE)
        gl_ = Star(n=5, outer_radius=0.14, color=C.BITS, fill_opacity=1).move_to(cells[goal[0] * n + goal[1]])
        tag = note(r"schematic").to_corner(DL, buff=0.25)
        items = VGroup(label(r"Turing, 1950: \ can machines think?", font_size=24, color=GREY_A),
                       label(r"search: \ A* and its proof", font_size=24, color=C.BITS),
                       label(r"games: \ minimax and alpha--beta", font_size=24, color=GREY_A),
                       label(r"logic, \ SAT and its phase transition", font_size=24, color=GREY_A),
                       label(r"expert systems, \ ELIZA, \ and the winters", font_size=24, color=GREY_A))
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Next time: the other road to intelligence, the one that came first. Alan Turing's question; machines "
            "that search, uniformly, <bookmark mark='a'/> or guided toward a goal; programs that play games and "
            "prove theorems; the expert systems; and the winters that followed. The symbolic era."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(st_), FadeIn(gl_), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(it) for it in items], lag_ratio=0.4), run_time=2.0)
            for r in range(1, 9):
                self.play(*[cells[i * n + j].animate.set_fill(GREY_B, 0.6) for i in range(n) for j in range(n)
                            if dist[i, j] == r], run_time=0.25)
            vo.wait_until("a")
            for i in range(n):
                for j in range(n):
                    cells[i * n + j].set_fill("#141A24", 1)
            for r in range(1, 13):
                self.play(*[cells[i * n + j].animate.set_fill(C.BITS, 0.75) for i in range(n) for j in range(n)
                            if dist[i, j] == r and dist[i, j] + h[i, j] <= 12 + 2], run_time=0.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"T.~M.~Cover \& J.~A.~Thomas, \textit{Elements of Information Theory}, 2nd ed.\ (2006), chapters 2, 3, 5, 13",
            r"D.~J.~C.~MacKay, \textit{Information Theory, Inference, and Learning Algorithms} (2003), chapters 2, 4--6",
            r"C.~M.~Bishop \& H.~Bishop, \textit{Deep Learning: Foundations and Concepts} (2024), chapter 2",
        ]
        papers = [
            r"R.~V.~L.~Hartley, \textit{Transmission of Information} (1928); \ C.~E.~Shannon, \textit{A Mathematical "
            r"Theory of Communication} (1948) and \textit{Prediction and Entropy of Printed English} (1951)",
            r"L.~G.~Kraft (1949); \ B.~McMillan, \textit{Two Inequalities Implied by Unique Decipherability} (1956); \ "
            r"D.~A.~Huffman (1952)",
            r"B.~McMillan, \textit{The Basic Theorems of Information Theory} (1953); \ L.~Breiman (1957); \ "
            r"S.~Kullback \& R.~A.~Leibler (1951)",
            r"P.-S.~Laplace, \textit{Essai philosophique sur les probabilit\'es} (1814); \ R.~A.~Fisher (1922)",
            r"J.~Rissanen (1976); \ R.~Pasco (1976); \ I.~H.~Witten, R.~M.~Neal \& J.~G.~Cleary, \textit{Arithmetic "
            r"Coding for Data Compression} (1987)",
            r"T.~M.~Cover \& R.~C.~King (1978); \ H.~W.~Lin \& M.~Tegmark (2017)",
            r"G.~Del\'etang et al., \textit{Language Modeling Is Compression} (ICLR 2024); \ Y.~Huang et al., "
            r"\textit{Compression Represents Intelligence Linearly} (COLM 2024); \ the Hutter Prize (2006--)",
            r"A.~Radford et al., GPT-2 (2019); \ Qwen Team, \textit{Qwen3 Technical Report} (2025)",
        ]
        card = reference_card(books, papers, font_size=19)
        data = note(r"Text: Project Gutenberg (30 novels; \textit{The Maltese Falcon}, eBook \#77600). \ Every "
                    r"number on screen is computed or cited; \ schematics are labeled.", font_size=18).to_edge(DOWN, buff=0.2)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=18)
        credit.next_to(data, UP, buff=0.08)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.12:
            card.scale((card.height - (credit.get_top()[1] + 0.12 - card.get_bottom()[1])) / card.height)
            card.next_to(credit, UP, buff=0.12)
        with self.voiceover(
            "This part followed the first chapters of Cover and Thomas's Elements of Information Theory, and "
            "MacKay's Information Theory, Inference, and Learning Algorithms, both of which go much further. The "
            "papers are all worth reading, starting with Shannon's two. Thanks for watching, and see you in Part 2."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
