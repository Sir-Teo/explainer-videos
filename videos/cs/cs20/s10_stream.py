from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, code, grid_table, load, mono, words)


class Stream(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.reservoir()
        self.misra_gries()
        self.count_min()
        self.guarantee()

    def card(self):
        card = chapter_card(9, r"Streams: \ one pass, \ little memory", r"What can you remember about data you "
                            r"can't keep?", lit=(1985, 2005), extra=((1985, r"reservoir sampling"),
                                                                     (2005, r"the Count-Min sketch")), part=PART)
        with self.voiceover((
            'Chapter nine. Streams: one pass, little memory.'
        )):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def model(self):
        d = load("stream")
        head = label(r"The streaming model", font_size=36).to_edge(UP, buff=0.4)
        toks = VGroup(*[label(rf"\texttt{{{w}}}", font_size=22, color=DATA) for w in
                        ("it", "was", "the", "best", "of", "times", "it", "was", "the", "worst", "of")])
        toks.arrange(RIGHT, buff=0.3).move_to(UP * 1.2)
        arrow = Arrow(toks.get_right() + RIGHT * 0.1, toks.get_right() + RIGHT * 1.3, color=GREY_B)
        box = VGroup(RoundedRectangle(width=2.4, height=1.1, corner_radius=0.1, stroke_color=HEAD),
                     label(r"a few KB", font_size=22, color=HEAD)).next_to(toks, DOWN, buff=0.8)
        rules = VGroup(
            label(rf"the items arrive one at a time: \ here, \ {words(d['N'])} words", font_size=22, color=WHITE),
            label(r"each is seen once, \ and can't be kept", font_size=22, color=WHITE),
            label(r"memory far smaller than the stream, \ or even than the number of distinct items", font_size=22,
                  color=HEAD),
            label(r"routers, \ sensors, \ logs, \ query planners: \ data that goes by too fast to store", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            (
            "Part 17 kept every distinct word of the novels, almost fifty-eight thousand. What if we can't afford "
            "that? <bookmark mark='a'/> In the streaming model the items go by once, <bookmark mark='b'/> can't be "
            "stored, <bookmark mark='c'/> and memory is far smaller than the stream, often smaller than the number "
            "of different items in it. <bookmark mark='d'/> Routers, sensors, logs and query planners live in this "
            'world.'
        )
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=LEFT * 0.3) for t in toks], lag_ratio=0.1),
                      GrowArrow(arrow), FadeIn(box))
            for mk, r in zip("abcd", rules):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.wait(0.3)
        self.clear_scene()

    def reservoir(self):
        d = load("stream")
        head = label(r"A uniform sample, \ without knowing the length", font_size=34).to_edge(UP, buff=0.35)
        prog = code([
            "keep the first k items",
            "for the i-th item, i > k:",
            "    with probability k / i:",
            "        it replaces a random one of the k",
        ], size=22).next_to(head, DOWN, buff=0.4)
        proof = VGroup(
            label(r"claim: \ after $i$ items, \ each is in the sample with probability $k/i$", font_size=21,
                  color=WHITE),
            MathTex(r"\frac{k}{i} \cdot \left(1 - \frac{k}{i+1} \cdot \frac{1}{k}\right) = \frac{k}{i} \cdot "
                    r"\frac{i}{i+1} = \frac{k}{i+1}", font_size=32, color=YES),
            label(r"(stay, \ unless the next item comes in \textbf{and} picks your slot)", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(prog, DOWN, buff=0.35)
        counts = d["counts"]
        top = max(counts)
        bars = VGroup(*[Rectangle(width=0.1, height=1.4 * c / top, stroke_width=0, fill_color=LAM, fill_opacity=0.85)
                        for c in counts]).arrange(RIGHT, buff=0.02, aligned_edge=DOWN).to_edge(DOWN, buff=0.7)
        exp = DashedLine(bars.get_left() + UP * 1.4 * d["expect"] / top, bars.get_right() + UP * 1.4 * d["expect"] / top,
                         color=HEAD).shift(DOWN * (bars.get_bottom()[1] - bars.get_bottom()[1]))
        exp.set_y(bars.get_bottom()[1] + 1.4 * d["expect"] / top)
        cap = label(rf"{d['trials']:,} runs, \ $k = {d['k']}$ of {d['of']}: \ each item chosen "
                    rf"{d['counts_min']:,}--{d['counts_max']:,} times \ (expected {d['expect']:,.0f})".replace(",", "{,}"),
                    font_size=18, color=GREY_A).next_to(bars, DOWN, buff=0.12)
        samp = label(r"eight words drawn from the novels in one pass: \ " + r", \ ".join(
            rf"\textit{{{w}}}" for w in d["sample"]), font_size=18, color=DATA).next_to(bars, UP, buff=0.15)
        with self.voiceover(
            (
            "First, a fair sample. We want k items chosen uniformly from the stream, but we don't know how long it "
            "will be. <bookmark mark='a'/> Reservoir sampling, as Jeffrey Vitter described it in 1985: keep the "
            'first k. When the i-th item arrives, keep it with probability k over i, throwing out a random one of '
            "the k. <bookmark mark='b'/> By induction, every item seen so far is in the sample with probability "
            'exactly k over i. An item stays when the next one arrives unless the newcomer is kept and picks its '
            "slot, and the arithmetic turns k over i into k over i plus one. <bookmark mark='c'/> We drew five items"
            ' from a hundred, fifty thousand times: every item was picked close to the expected two thousand five '
            "hundred times. <bookmark mark='d'/> And here are eight words drawn uniformly from all four million six "
            'hundred thousand in the novels, in a single pass.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(prog))
            vo.wait_until("a")
            self.play(Indicate(prog, color=HEAD))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in proof], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), Create(exp), FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeIn(samp))
        self.wait(0.3)
        self.clear_scene()

    def misra_gries(self):
        d = load("stream")
        head = label(rf"Misra--Gries: \ heavy hitters with {d['mg_k'] - 1} counters", font_size=34
                     ).to_edge(UP, buff=0.35)
        prog = code([
            "a word with a counter: add 1",
            "a new word, and a free counter: start it at 1",
            "a new word, no free counter:",
            "    subtract 1 from every counter; drop the zeros",
        ], size=20).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        why = VGroup(
            label(r"each subtraction removes $k$ words at once \ (the new one and $k - 1$ others)", font_size=19,
                  color=WHITE),
            label(r"so it happens at most $n/k$ times", font_size=19, color=WHITE),
            MathTex(r"f_x - \tfrac{n}{k} \le \text{count}(x) \le f_x", font_size=30, color=YES),
            label(r"every word with $f_x > n/k$ survives", font_size=19, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.4)
        rows = [[r["word"], words(r["true"]), words(r["mg"]) if r["mg"] else r"---"] for r in d["mg"][:16]]
        tab = grid_table([r"word", r"true count", r"Misra--Gries"], rows, widths=[1.6, 2.2, 2.4], row_h=0.24,
                         font_size=16, mono_cols=(0,),
                         colors=[[DATA, GREY_A, YES if r["true"] > d["mg_bound"] else NO] for r in d["mg"][:16]])
        tab.to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.8)
        note_ = label(rf"$n/k = {words(round(d['mg_bound']))}$: \ the thirteen words above it survive, \\ each "
                      r"undercounted by about 38{,}700; \\ a second pass counts the survivors exactly", font_size=19,
                      color=GREY_A).next_to(why, DOWN, buff=0.45)
        with self.voiceover(
            (
            "Next, the frequent items, the Job's own question. <bookmark mark='a'/> Jayadev Misra and David Gries "
            'gave a deterministic method in 1982, with k minus one counters. A word that has a counter adds one. A '
            'new word takes a free counter. A new word with no free counter subtracts one from every counter, and '
            "the counters that reach zero are freed. <bookmark mark='b'/> Each subtraction cancels k words at once, "
            'the new one and one from each counter, so it can happen at most n over k times. So every count is low '
            "by at most n over k, and any word more frequent than n over k must survive. <bookmark mark='c'/> With "
            'ninety-nine counters on the novels, n over k is about forty-six thousand. The thirteen words above that'
            ' all survived, each undercounted by about thirty-nine thousand, and words below it may vanish. A second'
            ' pass, counting only the survivors, makes the counts exact. But the estimates themselves are poor. Can '
            'coin flips do better?'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(prog))
            vo.wait_until("a")
            self.play(Indicate(prog, color=HEAD))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(w) for w in why], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.1))
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def count_min(self):
        head = label(r"The Count-Min sketch", font_size=36).to_edge(UP, buff=0.35)
        d_, w_ = 4, 10
        grid = VGroup()
        vals = [[3, 0, 5, 1, 0, 2, 7, 0, 1, 4], [1, 6, 0, 2, 3, 0, 1, 5, 2, 3], [0, 2, 4, 0, 8, 1, 0, 3, 1, 4],
                [2, 1, 0, 5, 1, 3, 2, 0, 6, 3]]
        for r in range(d_):
            row = VGroup(*[VGroup(Square(side_length=0.48, stroke_color=GREY_C, stroke_width=1.2),
                                  mono(str(vals[r][c]), 16, GREY_A)) for c in range(w_)]).arrange(RIGHT, buff=0)
            for cell in row:
                cell[1].move_to(cell[0])
            grid.add(row)
        grid.arrange(DOWN, buff=0).move_to(LEFT * 2.2 + DOWN * 0.2)
        rlab = VGroup(*[MathTex(rf"h_{r + 1}", font_size=26, color=LAM).next_to(grid[r], LEFT, buff=0.2)
                        for r in range(d_)])
        word = label(r"\texttt{whale}", font_size=28, color=DATA).next_to(grid, UP, buff=0.8)
        hit = [2, 7, 4, 8]
        arrows = VGroup(*[Arrow(word.get_bottom(), grid[r][hit[r]].get_top(), buff=0.05, stroke_width=2, color=DATA,
                                max_tip_length_to_length_ratio=0.05) for r in range(d_)])
        side = VGroup(
            label(r"$d$ rows of $w$ counters, \ one hash function per row", font_size=21, color=WHITE),
            label(r"\textbf{add} $x$: \ $+1$ at $h_r(x)$ in every row", font_size=21, color=DATA),
            label(r"\textbf{estimate} $x$: \ the \textbf{minimum} of its $d$ counters", font_size=21, color=YES),
            label(r"other words only ever add: \ never an undercount", font_size=21, color=GREY_A),
            label(r"Cormode and Muthukrishnan, \ 2005", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.2)
        with self.voiceover(
            (
            "Graham Cormode and S. Muthukrishnan's Count-Min sketch, from 2005, keeps a small table: d rows of w "
            "counters, with an independent hash function for each row. <bookmark mark='a'/> To add a word, hash it "
            "once per row and add one to each of those counters. <bookmark mark='b'/> To estimate a word's count, "
            "look at the same d counters and take the smallest. <bookmark mark='c'/> Every counter holds the word's "
            'true count plus the counts of whatever other words collided with it there. Collisions only ever add, so'
            ' the estimate is never too low, and the minimum picks the row with the fewest collisions.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(rlab), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(word), *[GrowArrow(a) for a in arrows], FadeIn(side[1]))
            self.play(*[Transform(grid[r][hit[r]][1], mono(str(vals[r][hit[r]] + 1), 16, DATA).move_to(
                grid[r][hit[r]][0])) for r in range(d_)],
                *[grid[r][hit[r]][0].animate.set_fill(DATA, 0.25) for r in range(d_)])
            vo.wait_until("b")
            self.play(FadeIn(side[2]), Indicate(grid[0][hit[0]], color=YES))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def guarantee(self):
        d = load("stream")
        c = d["cm"]["4x1021"]
        c2 = d["cm"]["2x1021"]
        head = label(r"How wrong can the minimum be?", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"with pairwise independent hashes, \ the excess in one row has", font_size=21, color=WHITE),
            MathTex(r"\mathbb{E}[\text{excess}] \le \frac{N}{w} \quad\Longrightarrow\quad "
                    r"\Pr\Big[\text{excess} \ge \frac{eN}{w}\Big] \le \frac1e \quad \text{(Markov)}", font_size=32,
                    color=LAM),
            label(r"the minimum is that bad only if \textbf{every} row is: \ independent rows", font_size=21,
                  color=WHITE),
            MathTex(r"w = \lceil e/\varepsilon\rceil,\ d = \lceil\ln(1/\delta)\rceil: \qquad \Pr[\hat f_x > f_x + \varepsilon N] "
                    r"\le e^{-d} = \delta", font_size=34, color=YES),
            label(r"memory $\frac{e}{\varepsilon} \ln \frac1\delta$ counters, \ whatever the number of distinct "
                  r"words", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.4)
        meas = VGroup(
            label(rf"the novels, \ $4 \times 1021$: \ $eN/w = {words(round(c['bound']))}$; \ "
                  rf"no word exceeded it; \ mean excess {words(round(c['mean_err']))}", font_size=20, color=YES),
            label(rf"two rows: \ {c2['over_bound'] * 100:.2f}\% of vocabulary exceeds the level; \ concrete hashes are empirical", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            f"How large can the error be in the standard insertion-only Count-Min model? <bookmark mark='a'/> In one "
            f'row, use a hash family with collision probability at most one over w for each pair. The expected excess'
            f' for a fixed queried item is at most N over w. Markov bounds excess above e times that by one over e. '
            f"<bookmark mark='b'/> With independently chosen row hashes, all rows must fail, so the probabilities "
            f"multiply. <bookmark mark='c'/> Choose width at least e over epsilon and depth at least the natural log "
            f'of one over delta. Each fixed item then has additive error at most epsilon N with probability at least '
            f'one minus delta. This is not a simultaneous guarantee for every item without an additional union bound.'
            f" <bookmark mark='d'/> The counter count depends on epsilon and delta; each counter still needs enough "
            f"bits for N. <bookmark mark='e'/> The corpus experiment has a comparison level of "
            f"{words(round(c['bound']))}"
            f' and mean excess about '
            f"{words(round(c['mean_err']))}"
            f'. Its concrete polynomial and double hashes are an empirical implementation, not a proof that the '
            f'independent-row theorem applies. The reported fraction across words is not a failure probability over '
            f'independent hash choices.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, ln in zip("abcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(meas))
        self.wait(0.3)
        self.clear_scene()
