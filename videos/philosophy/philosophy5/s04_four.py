from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403

PAIR = {"t": "(1, 0)", "f": "(0, 1)", "b": "(1, 1)", "n": "(0, 0)"}
WORD = {"t": r"told true only", "f": r"told false only", "b": r"told both", "n": r"told nothing"}


def diamond(top, left, right, bottom, center, title, up_label, size=1.45, font_size=34):
    """A Hasse diagram of FOUR: four discs in a diamond, edges, an axis arrow with its name."""
    c = np.asarray(center, float)
    pos = {top: c + UP * size, bottom: c + DOWN * size, left: c + LEFT * size, right: c + RIGHT * size}
    nodes = {}
    for v, p in pos.items():
        disc = Circle(radius=0.36, stroke_color=VAL_COLOR[v], stroke_width=3, fill_color=VAL_COLOR[v],
                      fill_opacity=0.2).move_to(p)
        nodes[v] = VGroup(disc, MathTex(vtex(v), font_size=font_size, color=VAL_COLOR[v]).move_to(p))
    edges = VGroup(*[Line(nodes[a][0].get_center(), nodes[b][0].get_center(), buff=0.38, color=GREY_B,
                          stroke_width=2.5) for a, b in ((bottom, left), (bottom, right), (left, top), (right, top))])
    ax = Arrow(c + LEFT * (size + 0.9) + DOWN * size, c + LEFT * (size + 0.9) + UP * size, buff=0, color=GREY_C,
               stroke_width=3)
    axl = label(up_label, font_size=22, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT, buff=0.12)
    t = label(title, font_size=28, color=P.CLAIM).next_to(VGroup(*nodes.values()), UP, buff=0.4)
    g = VGroup(edges, *nodes.values(), ax, axl, t)
    g.nodes, g.edges, g.title = nodes, edges, t
    return g


class Four(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Told true, told false", r"How should a computer think when its sources disagree?",
                            lit=(1977,), part=PART)
        with self.voiceover("Chapter three. Told true, told false."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.belnap()
        self.database()
        self.lattices()
        self.fde()

    def belnap(self):
        hcs = VGroup(history_card(1976, r"J.\ Michael Dunn", r"`Intuitive semantics for first-degree entailments'",
                                  width=5.6, color=HIST),
                     history_card(1977, r"Nuel Belnap", r"`How a computer should think'", width=5.0, color=HIST)
                     ).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        cells = VGroup()
        for v in "tbnf":
            box = RoundedRectangle(width=3.0, height=1.5, corner_radius=0.15, stroke_color=VAL_COLOR[v],
                                   stroke_width=2.5, fill_color=VAL_COLOR[v], fill_opacity=0.08)
            t = VGroup(MathTex(vtex(v), font_size=44, color=VAL_COLOR[v]),
                       MathTex(PAIR[v], font_size=28, color=GREY_A),
                       label(WORD[v], font_size=22)).arrange(DOWN, buff=0.1)
            cells.add(VGroup(box, t.move_to(box)))
        cells.arrange_in_grid(2, 2, buff=0.35).move_to([-3.4, -1.1, 0])
        key = VGroup(label(r"a value is a pair:", font_size=26, color=GOAL),
                     MathTex(r"(\text{told true},\ \text{told false})", font_size=34),
                     label(r"truth is what the computer has been told,", font_size=22, color=GREY_A),
                     label(r"not how the world is", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.2).move_to(
            [3.3, -1.0, 0])
        with self.voiceover(
            "In 1976 Michael Dunn found an intuitive semantics for a logic Anderson and Belnap had defined by "
            "axioms, and in 1977 Nuel Belnap turned it into a design for computers. <bookmark mark='a'/>A computer "
            "that collects information from many sources is told things. About each sentence it may have been told "
            "that it is true, or that it is false. <bookmark mark='b'/>So a value is a pair: told true, yes or no, "
            "and told false, yes or no. <bookmark mark='c'/>Four values. T: told true only. F: told false only. "
            "B: told both, because two sources conflict. N: told nothing at all. Truth here is not how the world "
            "is, but the state of the computer's information."
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("a")
            self.play(FadeIn(key[2:]))
            vo.wait_until("b")
            self.play(FadeIn(key[:2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in cells], lag_ratio=0.3))
        self.clear_scene()

    def database(self):
        d = load("database")
        told = VGroup(label(r"source 1: \ the door is open; \ the safe is locked", font_size=24),
                      label(r"source 2: \ the door is not open", font_size=24),
                      label(r"nobody mentions the light", font_size=24, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UL, buff=0.5)
        atoms = VGroup(*[VGroup(MathTex(a, font_size=34), MathTex("=", font_size=30), vmob(v, 34)).arrange(
            RIGHT, buff=0.15) for a, v in (("o", d["told"]["o"]), ("s", d["told"]["s"]), ("l", d["told"]["l"]))]
                       ).arrange(RIGHT, buff=0.8).next_to(told, DOWN, buff=0.4).align_to(told, LEFT)
        hd = [label(r"query", font_size=24, color=P.CLAIM), label(r"FDE", font_size=24, color=P.CLAIM)]
        rows = [[mxf(r["q"], 32), vmob(r["value"], 32)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[2.6, 1.4], cell_h=0.55, font_size=26).move_to([3.6, -0.3, 0])
        cl = label(r"classically: \ $o$ and $\lnot o$ entail everything, \ even $\lnot s$ \ (`the safe is open')",
                   font_size=24, color=BAD).to_edge(DOWN, buff=0.75)
        fd = label(r"in FDE: \ the conflict stays where it is; \ $\lnot s$ is F", font_size=24, color=OK).to_edge(
            DOWN, buff=0.3)
        bn = rows[[r["q"] for r in d["rows"]].index("o | l")][1]
        with self.voiceover(
            "Here is Belnap's computer at work. <bookmark mark='a'/>One source says the door is open and the safe is "
            "locked. Another says the door is not open. Nobody mentions the light. <bookmark mark='b'/>So the door "
            "is B, the safe is T, the light is N. <bookmark mark='c'/>Now ask questions. Is the door open? B. Is it "
            "both open and not open? Also B: it was told both. Is the light on or off? N: the computer was told "
            "nothing, and 'on or off' is not a fact it has been given. <bookmark mark='d'/>A surprise: 'the door is "
            "open, or the light is on' is plain T. One disjunct was told true, and nothing told the disjunction "
            "false. <bookmark mark='e'/>A classical database that believed both reports would believe everything, "
            "including that the safe is open. <bookmark mark='f'/>In the four-valued logic the conflict stays "
            "local: 'the safe is not locked' comes out F."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in told], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(atoms))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][0]) for r in range(len(rows))])
            self.play(LaggedStart(*[FadeIn(grid.cell[r][1]) for r in range(len(rows)) if rows[r][1] is not bn],
                                  lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(bn, scale=0.6), Indicate(grid.cell[[r["q"] for r in d["rows"]].index("o | l")][0]))
            vo.wait_until("e")
            self.play(FadeIn(cl))
            vo.wait_until("f")
            self.play(FadeIn(fd))
        self.clear_scene()

    def lattices(self):
        d = load("four")
        tr = diamond("t", "b", "n", "f", [-3.4, -0.5, 0], r"the truth order", r"more true")
        inf = diamond("b", "t", "f", "n", [3.4, -0.5, 0], r"the information order", r"more told")
        meet = MathTex(r"\land = \text{meet}, \quad \lor = \text{join}", font_size=30, color=GOAL).next_to(
            tr, DOWN, buff=0.35)
        cons = MathTex(r"\mathbf{T} \otimes \mathbf{F} = \mathbf{N} \ \ (\text{consensus}), \quad "
                       r"\mathbf{T} \oplus \mathbf{F} = \mathbf{B} \ \ (\text{gullibility})", font_size=26,
                       color=GREY_A).next_to(inf, DOWN, buff=0.35)
        neg = label(r"$\lnot$ turns the truth order upside down \ and leaves the information order alone", font_size=24,
                    color=GOAL).to_edge(DOWN, buff=0.3)
        bil = label(r"a \textit{bilattice}: \ two lattice orders on one set \ (Ginsberg 1988; Fitting 1991)",
                    font_size=24, color=GREY_B).to_edge(UP, buff=0.35)
        assert d["lattice"] and d["negation"]
        with self.voiceover(
            "The four values carry two orders at once. <bookmark mark='a'/>In the truth order, F is at the bottom "
            "and T at the top; B and N sit in between, incomparable. <bookmark mark='b'/>'And' is the meet in this "
            "order, the highest value below both, and 'or' is the join. The Reasoner checked every pair: the "
            "tables of the last chapters fall out of the picture. <bookmark mark='c'/>In the information order, "
            "N is at the bottom, knowing nothing, and B at the top, told everything. Its meet of T and F is N: what "
            "two sources agree on. Its join is B: everything either one said. <bookmark mark='d'/>Negation turns "
            "the truth order upside down and leaves information alone: denying a claim does not tell you more. "
            "<bookmark mark='e'/>A set with two such orders is a bilattice, a structure Matthew Ginsberg and "
            "Melvin Fitting developed for reasoning in artificial intelligence."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tr))
            vo.wait_until("b")
            self.play(FadeIn(meet))
            vo.wait_until("c")
            self.play(FadeIn(inf), FadeIn(cons))
            vo.wait_until("d")
            self.play(FadeIn(neg))
            vo.wait_until("e")
            self.play(FadeIn(bil))
        self.clear_scene()

    def fde(self):
        d = load("four")
        head = label(r"FDE: \ designate T and B, \ everything that was told true", font_size=30, color=CONN).to_edge(
            UP, buff=0.5)
        sub = VGroup(VGroup(label(r"drop B", font_size=26, color=GOAL), MathTex(r"\Rightarrow", font_size=30),
                            label(r"K3: \ gaps only", font_size=26)).arrange(RIGHT, buff=0.3),
                     VGroup(label(r"drop N", font_size=26, color=GOAL), MathTex(r"\Rightarrow", font_size=30),
                            label(r"LP: \ gluts only", font_size=26)).arrange(RIGHT, buff=0.3),
                     VGroup(label(r"drop both", font_size=26, color=GOAL), MathTex(r"\Rightarrow", font_size=30),
                            label(r"classical logic", font_size=26)).arrange(RIGHT, buff=0.3)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.8, 0.2, 0])
        taut = VGroup(label(r"FDE has no tautologies at all:", font_size=26, color=P.CLAIM),
                      label(r"make every atom N, \ and every formula is N", font_size=24),
                      label(r"and no explosion: \ make $p$ B and $q$ F", font_size=24),
                      label(r"what survives: \ De Morgan, \ double negation, \ $\land$ and $\lor$ rules", font_size=24,
                            color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.3, 0.2, 0])
        name = label(r"`first-degree entailment': \ exactly the valid $A \to B$ with no arrows inside $A$ or $B$ "
                     r"\ (Anderson and Belnap 1975)", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        assert d["tautologies"] == []
        with self.voiceover(
            "The logic of the four values is called FDE. <bookmark mark='a'/>It designates T and B: whatever the "
            "computer was told is true, whether or not it was also told the opposite. <bookmark mark='b'/>It "
            "contains the logics we already have. Remove B, and you get K3. Remove N, and you get LP. Remove both, "
            "and you are back to classical logic. <bookmark mark='c'/>FDE itself has no tautologies: make every "
            "atom N, and every formula is N. And no explosion: make p B and q F. <bookmark mark='d'/>What survives "
            "are the laws that only move information around: De Morgan's laws, double negation, and the rules for "
            "'and' and 'or'. <bookmark mark='e'/>The name, first-degree entailment, comes from Anderson and "
            "Belnap: these are exactly the valid conditionals with no conditional inside them."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.15) for s_ in sub], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(taut[:3]))
            vo.wait_until("d")
            self.play(FadeIn(taut[3]))
            vo.wait_until("e")
            self.play(FadeIn(name))
        self.clear_scene()
