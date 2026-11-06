from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Spinoza(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"The \textit{Ethics}, \ in geometrical order", r"Can metaphysics be proved like "
                            r"geometry?", lit=(1677,), part=PART)
        with self.voiceover("Chapter three. The Ethics, in geometrical order."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.book()
        self.graph()
        self.god()
        self.necessity()

    def book(self):
        d = load("ethics")
        hc = history_card(1677, r"Baruch Spinoza", r"\textit{Ethica, ordine geometrico demonstrata}, \ published after "
                          r"his death", width=6.0, color=HIST).to_corner(UL, buff=0.35)
        parts = VGroup(
            VGroup(label(r"8 definitions", font_size=28, color=KIND_COL["D"]),
                   label(r"self-caused; \ substance; \ attribute; \ mode;", font_size=20, color=GREY_A),
                   label(r"God; \ free; \ eternity", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.1),
            VGroup(label(r"7 axioms", font_size=28, color=KIND_COL["A"]),
                   label(r"`everything is in itself", font_size=20, color=GREY_A),
                   label(r"or in another'; \ \dots", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.1),
            VGroup(label(r"36 propositions", font_size=28, color=KIND_COL["P"]),
                   label(r"each with a demonstration", font_size=20, color=GREY_A),
                   label(r"citing what came before", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.1)).arrange(
            RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 0.6, 0])
        ex = VGroup(label(r"Prop.\ VII. \ \textit{Existence belongs to the nature of substances.}", font_size=24),
                    label(r"Proof: \ `Substance cannot be produced by anything external \ (Corollary, Prop vi.), \ it "
                          r"must, therefore, be its own cause \dots'", font_size=21, color=GREY_A)).arrange(
            DOWN, buff=0.15).move_to([0, -1.3, 0])
        src = label(rf"the Reasoner reads Elwes's translation of 1883 \ (Project Gutenberg) \ and finds "
                    rf"{len(d['edges'])} citations", font_size=22, color=OK).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Baruch Spinoza took Descartes's hope literally. <bookmark mark='a'/>His Ethics, published in 1677, just "
            "after his death, is demonstrated in geometrical order, like Euclid. <bookmark mark='b'/>Part One, "
            "Concerning God, begins with eight definitions, of things like substance, attribute, mode and God; then "
            "seven axioms; then thirty-six propositions, each with a demonstration that cites what came before. "
            "<bookmark mark='c'/>For example, Proposition 7: existence belongs to the nature of substance. Its proof "
            "cites the corollary to Proposition 6. <bookmark mark='d'/>So the book is a graph, and the Reasoner can "
            "build it. It reads the English translation of R. H. M. Elwes, from 1883, finds every citation in every "
            "demonstration, a hundred and two of them, and draws the result."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in parts], lag_ratio=0.5), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(ex))
            vo.wait_until("d")
            self.play(FadeIn(src))
        self.clear_scene()

    def graph(self):
        d = load("ethics")
        head = label(r"Ethics I, \ as the Reasoner reads it", font_size=28, color=CONN).to_edge(UP, buff=0.2)
        g = ethics_dag(d, top=2.6)
        g.shift(DOWN * 0.35)
        cols = sorted(g.cols)
        chain = d["chain"]
        chain_edges = VGroup(*[Line(g.pos[a], g.pos[b], color=GOAL, stroke_width=4).shift(DOWN * 0.35)
                               for a, b in zip(chain, chain[1:])])
        notes = VGroup(
            label(r"no circles: \ every demonstration cites only what came before", font_size=21, color=OK),
            label(rf"the longest chain: \ {len(chain) - 1} steps, \ from the definition of substance \ to "
                  rf"`will is not a free cause'", font_size=21, color=GOAL),
            label(r"most cited: \ substance (D3), \ God exists (P11), \ all is in God (P15), \ all follows from God "
                  r"(P16): \ 7 each", font_size=21, color=REASON),
            label(r"never cited: \ Axioms 2 and 7 \ (the Latin cites Axiom 7 in Prop.\ 11; \ Elwes dropped it)",
                  font_size=21, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.2)
        assert d["forward"] and d["unused"] == ["A2", "A7"] and d["unused_latin"] == ["A2"]
        with self.voiceover(
            "Here it is. <bookmark mark='a'/>The definitions and axioms stand in the first column, in blue and gold. "
            "Each proposition sits one column to the right of the deepest thing it relies on. <bookmark mark='b'/>"
            "The lines are the citations. <bookmark mark='c'/>The Reasoner checks the structure. There are no "
            "circles: every demonstration cites only what came before it, as in Euclid. <bookmark mark='d'/>The "
            "longest chain runs ten steps, from the definition of substance, through the proof that God exists, to "
            "Proposition 32: the will is not a free cause. <bookmark mark='e'/>The most cited items are the "
            "definition of substance, the existence of God, and the propositions that whatever is, is in God, and "
            "that infinitely many things follow from God's nature. <bookmark mark='f'/>And two axioms are never cited "
            "at all, the second and the seventh. The seventh is a translator's slip: in Spinoza's Latin, the first "
            "proof that God exists cites it, and Elwes's English leaves the citation out. A program found it by "
            "counting."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*[g.node[n] for n in g.cols[c]], *[g.label[n] for n in g.cols[c]]))
                                    for c in cols], lag_ratio=0.3), run_time=4)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(e) for e in g.edges], lag_ratio=0.01), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(e) for e in chain_edges], lag_ratio=0.3),
                      *[g.node[n].animate.scale(1.6).set_color(GOAL) for n in chain], FadeIn(notes[1]), run_time=3)
            vo.wait_until("e")
            self.play(*[Indicate(g.node[n], color=REASON, scale_factor=2.2) for n in ("D3", "P11", "P15", "P16")],
                      FadeIn(notes[2]))
            vo.wait_until("f")
            self.play(*[g.node[n].animate.set_color(BAD).scale(1.8) for n in ("A2", "A7")], FadeIn(notes[3]))
        self.wait(1)
        self.clear_scene()

    def god(self):
        d = load("ethics")
        head = label(r"What the proof of God rests on", font_size=30, color=CONN).to_edge(UP, buff=0.2)
        g = ethics_dag(d, top=2.6)
        g.shift(DOWN * 0.35)
        anc = set(d["ancestors_P11"])
        dim = [m for n, m in g.node.items() if n not in anc and n != "P11"]
        dimlab = [g.label[n] for n in g.node if n not in anc and n != "P11"]
        keep_edges = [e for (a, b), e in g.edge.items() if a in anc | {"P11"} and b in anc | {"P11"}]
        notes = VGroup(
            label(rf"Proposition 11, \ `God necessarily exists', \ rests on {len(anc)} items:", font_size=22,
                  color=GOAL),
            label(r"the definitions of substance and God, \ three axioms, \ and Propositions 2, 3, 6 and 7",
                  font_size=21, color=GREY_A),
            label(r"its heart: \ P7, \ existence belongs to the nature of substance: \ an ontological argument "
                  r"\ (Part 23)", font_size=21, color=REASON)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(
            DOWN, buff=0.25)
        assert len(anc) == 9
        with self.voiceover(
            "The graph also answers a question every reader of Spinoza asks: what does the proof of God's existence "
            "rest on? <bookmark mark='a'/>The Reasoner follows the citations of Proposition 11 back to their sources. "
            "<bookmark mark='b'/>Nine items: the definitions of substance and of God, three axioms, and Propositions "
            "2, 3, 6 and 7. Nothing else in the graph is needed for it. <bookmark mark='c'/>The heart is Proposition 7: "
            "existence belongs to the nature of substance. It is an ontological argument, from the concept of a thing "
            "to its existence, of the kind Part 23 examines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(*[m.animate.set_opacity(0.12) for m in dim + dimlab],
                      *[e.animate.set_stroke(opacity=0.05) for e in g.edges], run_time=1.5)
            vo.wait_until("b")
            self.play(*[e.animate.set_stroke(GOAL, width=2.5, opacity=0.9) for e in keep_edges],
                      *[g.node[n].animate.scale(1.6).set_color(GOAL) for n in anc | {"P11"}], FadeIn(notes[0]),
                      FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Indicate(g.node["P7"], color=REASON, scale_factor=2.0), FadeIn(notes[2]))
        self.clear_scene()

    def necessity(self):
        head = label(r"God, \ or Nature", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        rows = rows_at([
            (r"P14", r"besides God, \ no substance can be or be conceived"),
            (r"P15", r"whatever is, \ is in God"),
            (r"P29", r"nothing in nature is contingent"),
            (r"P33", r"things could not have been produced \ in any other way, \ or in any other order"),
        ], x_left=-5.6, x_right=-4.2, y0=1.6, dy=0.75, font_size=26, left_color=KIND_COL["P"])
        q = label(r"\textit{Deus sive Natura}: \ God, or Nature \ (Part IV): \ one substance, \ and everything a mode "
                  r"of it", font_size=24, color=GOAL).next_to(rows, DOWN, buff=0.5).set_x(0)
        tail = label(r"freedom, \ for Spinoza, \ is understanding that necessity \ (Part 32)", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "And what does the geometry prove? <bookmark mark='a'/>That besides God no substance can be or be "
            "conceived. <bookmark mark='b'/>That whatever is, is in God. <bookmark mark='c'/>That nothing in nature "
            "is contingent. <bookmark mark='d'/>And that things could not have been produced in any other way, or "
            "in any other order. <bookmark mark='e'/>Spinoza's phrase for the one substance is God, or Nature. "
            "Everything else is a mode of it, a way that it is. <bookmark mark='f'/>Freedom, for Spinoza, is not "
            "escape from this necessity, but understanding it, a thought Part 32 will weigh."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(q))
            vo.wait_until("f")
            self.play(FadeIn(tail))
        self.clear_scene()
