from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Graphs(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Knowledge graphs and embeddings", r"What does a learned representation commit "
                            r"to?", lit=(2012, 2013), part=PART)
        with self.voiceover("Chapter fifteen. Knowledge graphs and embeddings."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.embed()
        self.commit()
        self.llms()

    def embed(self):
        d = load("transe")
        head = label(r"TransE: \ relations as translations \ (Bordes et al., \ 2013)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.25)
        E = d["entities"]
        R = d["relations"]
        xs = np.array([v[0] for v in E.values()])
        ys = np.array([v[1] for v in E.values()])
        cx, cy = xs.mean(), ys.mean()
        s = 1.9 / max(np.abs(xs - cx).max(), np.abs(ys - cy).max())
        o = np.array([-2.8, -0.6, 0])

        def P(v):
            return o + np.array([(v[0] - cx) * s, (v[1] - cy) * s, 0])

        kinds = {"Europe": GOAL, "Asia": GOAL}
        caps = {"Paris", "Berlin", "Rome", "Madrid", "Lisbon", "Tokyo", "Seoul"}
        dots = VGroup()
        names = VGroup()
        for n, v in E.items():
            col = kinds.get(n, WHOLE if n in caps else UNIV)
            dots.add(Dot(P(v), radius=0.08, color=col))
            names.add(label(n, font_size=13, color=col).next_to(P(v), UR, buff=0.04))
        ex = [("Paris", "capital of"), ("France", "in"), ("Tokyo", "capital of"), ("Japan", "in")]
        arrows = VGroup(*[Arrow(P(E[h]), P(np.array(E[h]) + np.array(R[r])), buff=0.05, color=PARTC if r == "in"
                                else NOM, stroke_width=3, max_tip_length_to_length_ratio=0.15) for h, r in ex])
        f = MathTex(r"\mathbf h + \mathbf r \approx \mathbf t", font_size=40, color=GOAL).move_to([3.6, 2.0, 0])
        rows = stack([(r"each entity a point; \ each relation a displacement", WHITE),
                      (r"trained on " + f"{d['train']}" + r" triples, \ by pushing true ones close and corrupted ones "
                       r"apart", GREY_A),
                      (r"two dimensions here; \ hundreds in practice", GREY_A)], font_size=19, aligned_edge=LEFT,
                     width=5.4).move_to([3.6, 0.4, 0])
        leg = VGroup(label(r"capital of", font_size=15, color=NOM), label(r"in", font_size=15, color=PARTC)).arrange(
            RIGHT, buff=0.5).next_to(rows, DOWN, buff=0.3)
        with self.voiceover(
            "Knowledge graphs store facts as triples: Paris, capital of, France; France, in, Europe. Wikidata holds "
            "more than a hundred million items; Google's Knowledge Graph was announced in 2012. "
            "<bookmark mark='a'/>Machine learning represents them geometrically. In TransE, from Antoine Bordes and "
            "colleagues, each entity is a point and each relation a displacement, so a triple is plausible when the "
            "head plus the relation lands near the tail. <bookmark mark='b'/>The Reasoner trains one in two "
            "dimensions on thirteen triples about capitals, countries and continents. <bookmark mark='c'/>Capital-of "
            "is roughly one arrow, the same from Paris and from Tokyo; in is another."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.05), FadeIn(names), FadeIn(rows[1]),
                      FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), FadeIn(leg))
        self.clear_scene()

    def commit(self):
        d = load("transe")
        head = label(r"An embedding answers everything", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        tk = d["tokyo_in"]
        held = d["held_top"]
        eu = d["europe_capital_of"]
        hd = [r"\text{query}", r"\text{in the graph?}", r"\text{the embedding's answer}"]
        rows = [[MathTex(r"\text{Tokyo, in, ?}", font_size=22), MathTex(r"\text{no (inferable)}", font_size=20,
                                                                       color=GREY_A),
                 MathTex(r"\text{" + tk[0][0] + r"}", font_size=22, color=OK)],
                [MathTex(r"\text{" + d['held_out'][0] + r", capital of, ?}", font_size=22),
                 MathTex(r"\text{held out}", font_size=20, color=GREY_A),
                 MathTex(r"\text{" + held[0][0] + r" (truth ranked " + f"{d['held_rank']}" + r" of 7)}",
                         font_size=22, color=BAD)],
                [MathTex(r"\text{Europe, capital of, ?}", font_size=22), MathTex(r"\text{nonsense}", font_size=20,
                                                                                color=GREY_A),
                 MathTex(r"\text{" + eu[0][0] + r"}", font_size=22, color=BAD)]]
        grid = ValueGrid(hd, rows, col_w=[3.6, 2.6, 4.6], cell_h=0.62, font_size=20).move_to([0, 1.0, 0])
        notes = stack([(r"it scores all " + f"{d['possible_triples']}" + r" possible triples: \ it never says "
                        r"`unknown'", GOAL),
                       (r"right where structure supports it; \ confident where the data are silent; \ an answer even "
                        r"to nonsense", BAD),
                       (r"a description logic, \ by contrast, \ leaves the unentailed open \ (chapter 13)", UNIV),
                       (r"its ontological commitment: \ whatever its geometry ranks highest", GREY_A)],
                      font_size=19, width=12.4).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now ask the embedding questions. <bookmark mark='a'/>Where is Tokyo? The graph never says, but Tokyo is "
            "the capital of Japan and Japan is in Asia, and the geometry gets it right: Asia. "
            "<bookmark mark='b'/>Which country has Lisbon as its capital? That triple was held out, and it was "
            "Lisbon's only fact, so the embedding has no evidence at all. It answers anyway, Germany, and ranks the "
            "truth near the bottom. <bookmark mark='c'/>Europe is the capital of what? A nonsense question; it answers "
            "Korea. <bookmark mark='d'/>An embedding assigns a score to every one of the five hundred and twelve "
            "possible triples. It never says unknown. <bookmark mark='e'/>It is right where structure supports it, "
            "confident where the data are silent, and answers even nonsense. <bookmark mark='f'/>A description logic, "
            "with its open world, would leave the unentailed open. <bookmark mark='g'/>In Quine's terms, the "
            "embedding's commitments are whatever its geometry ranks highest, which is far more than anyone told it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, i in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*grid.cell[i])))
            for mk, r in zip("defg", notes):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def llms(self):
        head = label(r"What does a language model say there is?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"implicit ontology", r"a language model has no explicit TBox; \ its categories live in its weights", UNIV),
            (r"probing", r"Othello-GPT \ (Li et al., \ 2023): \ trained only on moves, \ it represents the board, \ "
                         r"recoverable and causally used", OK),
            (r"world models?", r"is that representation a commitment to boards, \ or just a useful compression?",
             GOAL),
            (r"Quine's test", r"what must its variables range over for its outputs to be true? \ we cannot yet read "
                              r"them off", BAD),
            (r"onward", r"representation and meaning \ (Parts 27 and 28); \ minds \ (Part 30); \ alignment \ (Part 42)",
             GREY_A),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Large language models raise the question again. <bookmark mark='a'/>A language model has no explicit "
            "terminology. Whatever categories it uses live implicitly in its weights. <bookmark mark='b'/>Probing can "
            "find some of them. A model trained only on sequences of Othello moves turned out to represent the board, "
            "in a form that can be read out and that the model actually uses. <bookmark mark='c'/>Is that a "
            "commitment to boards, or only a useful compression of the data? <bookmark mark='d'/>Quine's test asks what "
            "a theory's variables must range over for it to be true. For a neural network, we cannot yet read the "
            "variables off. <bookmark mark='e'/>Representation and meaning return in Parts 27 and 28, minds in Part "
            "30, and the alignment of such systems in the finale."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
