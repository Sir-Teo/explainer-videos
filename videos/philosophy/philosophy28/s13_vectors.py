from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403

GROUPS = {"animal": (["cat", "dog", "mouse", "bird"], WORD), "royal": (["king", "queen", "prince", "princess"], USE),
          "city": (["paris", "rome", "london", "berlin"], WORLD), "food": (["cheese", "bread", "butter", "milk"], HEAR),
          "person": (["holmes", "watson", "frodo", "darwin", "newton", "dickens"], TRUTH)}


class Vectors(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"You shall know a word", r"Is meaning distribution?", lit=(1954, 1957),
                            part=PART)
        with self.voiceover("Chapter twelve. You shall know a word."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.hypothesis()
        self.build()
        self.space()
        self.analogy()

    def hypothesis(self):
        q = quote_card(r"You shall know a word by the company it keeps.", r"J. R. Firth",
                       r"`A Synopsis of Linguistic Theory' \ (1957)", width=8.4, font_size=28).to_edge(UP, buff=0.6)
        rows = [
            (r"Saussure", r"a sign's value is its differences from other signs: \ meaning is relational \ (1916)", HIST),
            (r"Harris \ (1954)", r"words that occur in the same contexts tend to have similar meanings: \ the "
                                 r"distributional hypothesis", WORD),
            (r"the bet", r"collect contexts, \ count, \ compress: \ similarity of meaning becomes nearness in a space",
             USE),
            (r"\textit{AI, Built}", r"Part 3 built word vectors this way, \ and every language model since extends it",
             RULE_C),
        ]
        g = rows_table(rows, top=0.6, gap=0.45, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "A different idea of meaning came from structural linguistics. <bookmark mark='a'/>Ferdinand de Saussure "
            "taught that a sign has its value through its differences from other signs: meaning is relational. "
            "<bookmark mark='b'/>Zellig Harris, in 1954, made it measurable: words that occur in the same contexts tend "
            "to have similar meanings. <bookmark mark='c'/>John Firth put it as a slogan in 1957: you shall know a word "
            "by the company it keeps. <bookmark mark='d'/>The bet is that if you collect contexts, count them and "
            "compress the counts, similarity of meaning becomes nearness in a space. <bookmark mark='e'/>Part 3 of the "
            "AI series built word vectors this way, and every language model since extends the idea."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]))
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(g[2]))
            vo.wait_until("e")
            self.play(FadeIn(g[3]))
        self.clear_scene()

    def build(self):
        d = load("vectors")
        head = label(r"Word vectors, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        steps = stack([(rf"a corpus of {d['tokens']} words, \ {d['vocab']} distinct content words", WHITE),
                       (r"count, \ for each pair of words, \ how often they occur within two words of each other, \ in "
                        r"one sentence", WORD),
                       (r"reweight by positive pointwise mutual information: \ $\max\!\big(0,\ \log "
                        r"\tfrac{P(w, c)}{P(w)\,P(c)}\big)$", RULE_C),
                       (r"compress to six dimensions by singular value decomposition, \ and compare by cosine", USE)], font_size=20,
                      aligned_edge=LEFT, width=6.4, buff=0.28).move_to([-3.2, 0.6, 0])
        hd = [r"\text{word}", r"\text{nearest nouns}"]
        cells = [[label(w, font_size=20, color=TRUTH), label(r", \ ".join(f"{n} ({s:.2f})" for n, s in nb), font_size=18)]
                 for w, nb in d["nearest"].items()]
        grid = ValueGrid(hd, cells, col_w=[1.6, 4.6], cell_h=0.48, font_size=19).move_to([3.6, 0.4, 0])
        nb = {w: [x[0] for x in v] for w, v in d["nearest"].items()}
        assert nb["cat"] == ["dog", "bird", "mouse"] and nb["king"] == ["prince", "land", "crown"]
        assert nb["paris"] == ["train", "berlin", "rome"] and nb["cheese"] == ["butter", "seed", "bone"]
        assert d["k"] == 6
        foot = label(r"no definitions, \ no reference: \ only which words keep which company", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The Reasoner builds a tiny version. <bookmark mark='a'/>A small corpus: sentences about cats and dogs, "
            "kings and queens, cities, food, and some people, real and fictional. <bookmark mark='b'/>For every pair "
            "of words, count how often they occur near each other in a sentence. <bookmark mark='c'/>Reweight each "
            "count by how much more often the pair occurs than chance would predict, keeping only the positive "
            "excess. <bookmark mark='d'/>Compress the table to six dimensions by singular value decomposition, and "
            "compare words by the angle between their vectors. <bookmark mark='e'/>Among the nouns, the nearest "
            "neighbours of cat are dog, bird and mouse; of king, prince, land and crown; of Paris, the train and two "
            "other cities; of cheese, butter, seed and bone. "
            "<bookmark mark='f'/>No definitions were given and nothing was pointed at: only which words keep which "
            "company."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            vo.wait_until("e")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(cells)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def space(self):
        d = load("vectors")
        head = label(r"The space of words", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        xy = d["xy"]
        pts = np.array([xy[w] for w in xy])
        assert len(xy) == 22
        lo, hi = pts.min(0), pts.max(0)

        def P(p):
            u = (np.array(p) - lo) / np.where(hi - lo > 0, hi - lo, 1)
            return np.array([-6.0 + 7.4 * u[0], -2.9 + 5.4 * u[1], 0])

        dots = VGroup()
        for name, (ws, col) in GROUPS.items():
            pts_g = [P(xy[w]) for w in ws if w in xy]
            cen = np.mean(pts_g, axis=0)
            tight = max(np.linalg.norm(q - cen) for q in pts_g) < 0.6
            g = VGroup(*[Dot(q, radius=0.06, color=col) for q in pts_g])
            if tight:
                g.add(label(r", \ ".join(w for w in ws if w in xy), font_size=15, color=col).next_to(g, UP, buff=0.1))
            else:
                for j, (w, q) in enumerate(zip([w for w in ws if w in xy], pts_g)):
                    g.add(label(w, font_size=15, color=col).next_to(q, [UR, DR, UL, DL, RIGHT, LEFT][j % 6], buff=0.05))
            dots.add(g)
        legend = VGroup(*[label(n, font_size=19, color=c) for n, (ws, c) in GROUPS.items()]).arrange(
            DOWN, buff=0.22, aligned_edge=LEFT).move_to([5.6, 0.8, 0])
        foot = stack([(r"the vectors of these 22 words, \ projected onto their two main directions", GREY_A),
                      (r"kinds of word gather: \ the distribution carries a great deal of what we call meaning", OK)],
                     font_size=19, aligned_edge=LEFT, width=4.2, buff=0.2).move_to([5.0, -1.8, 0])
        with self.voiceover(
            "Take the vectors of these twenty-two words and project them onto their two main directions. "
            "<bookmark mark='a'/>Without being told "
            "anything about kinds, the words gather: animals together, royalty together, cities together, food "
            "together, people together. <bookmark mark='b'/>The distribution of words in text carries a great deal of "
            "what we call meaning. The question is whether it carries all of it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.05), FadeIn(legend), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def analogy(self):
        d = load("analogies")
        head = label(r"Relations as directions", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows_d = d["rows"]
        assert d["right"] == 1 and rows_d[0]["got"][0] == "queen"
        assert rows_d[1]["got"][0] == "rome" and rows_d[2]["got"][0] == "london" and rows_d[2]["got"][1] == "berlin"
        eq = MathTex(r"\vec{v}_{\text{king}} - \vec{v}_{\text{prince}} + \vec{v}_{\text{princess}} \;\approx\; "
                     r"\vec{v}_{\,?}", font_size=34, color=USE).move_to([0, 2.1, 0])
        hd = [r"a - b + c", r"\text{expected}", r"\text{nearest three}", r"\text{right?}"]
        cells = []
        for r in rows_d:
            cells.append([label(rf"{r['a']} $-$ {r['b']} $+$ {r['c']}", font_size=19, color=WORD),
                          label(r["want"], font_size=19, color=OK),
                          label(r", \ ".join(r["got"]), font_size=19, color=GREY_A),
                          MathTex(r"\checkmark" if r["right"] else r"\times", font_size=26,
                                  color=OK if r["right"] else BAD)])
        grid = ValueGrid(hd, cells, col_w=[4.4, 1.8, 3.6, 0.8], cell_h=0.55, font_size=20).move_to([0, 0.2, 0])
        foot = stack([(r"one of three: \ each city meets its country in a single sentence", BAD),
                      (r"word2vec \ (Mikolov et al., \ 2013) \ found such directions in billions of words", HIST),
                      (r"Saussure's point, \ in geometry: \ what a word means is where it stands among the others", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "If similar meanings are nearby points, perhaps relations between meanings are directions. "
            "<bookmark mark='a'/>Take the vector for king, subtract prince, and add princess. If the difference "
            "between king and prince is a direction, the result should land near queen. "
            "<bookmark mark='b'/>On the Reasoner's tiny vectors, it does. <bookmark mark='c'/>But London minus "
            "England plus France lands on Rome, not Paris, and Rome minus Italy plus Germany lands on London, with "
            "Berlin second. <bookmark mark='d'/>One of three. In this corpus each city meets its country in a single "
            "sentence, which is too little to carve out a direction. <bookmark mark='e'/>The word2vec models of "
            "Tomas Mikolov and colleagues, in 2013, found such directions reliably, in billions of words. "
            "<bookmark mark='f'/>It is Saussure's point, in geometry: what a word means is a matter of where it "
            "stands among the others."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[1]])
            self.play(*[FadeIn(c) for c in grid.cell[2]])
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
            vo.wait_until("f")
            self.play(FadeIn(foot[2]))
        self.clear_scene()
