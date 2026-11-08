from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class Arrhenius(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Impossibility", r"Can any ranking of populations meet every condition?", lit=(2000,),
                            part=PART)
        with self.voiceover("Chapter four. Impossibility."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theorem()
        self.search()
        self.sadism()
        self.examples()
        self.wall_brick()

    def theorem(self):
        hc = history_card(2000, r"Gustaf Arrhenius", r"``An Impossibility Theorem for Welfarist Axiologies''",
                          width=6.4, color=HIST).to_corner(UL, buff=0.3)
        rows = [(r"the idea", r"list conditions any acceptable ranking of populations should meet, \ each very hard to "
                              r"deny", GREY_A),
                (r"the result", r"no ranking meets them all: \ like Arrow's theorem of Part 39, \ but for "
                                r"populations", BAD),
                (r"later theorems", r"weaker and weaker conditions, \ still jointly impossible \ (Arrhenius, \ "
                                    r"\textit{Population Ethics}, \ forthcoming)", RISK),
                (r"built here", r"six conditions and five views; \ the Reasoner searches small populations for each "
                                r"violation", WELL)]
        g = rows_table(rows, top=1.0, gap=0.45, width=8.0, x_text=-2.2)
        with self.voiceover(
            "Every view so far has a cost. Gustaf Arrhenius showed, in 2000, that this is no accident. "
            "<bookmark mark='a'/>He listed conditions that any acceptable ranking of populations should meet, each "
            "very hard to deny: among them, avoiding the repugnant conclusion, avoiding what he called the sadistic "
            "conclusion, and a weak form of mere addition. <bookmark mark='b'/>He proved that no ranking meets them "
            "all: an impossibility theorem in the style of Arrow's theorem about voting, which Part 39 builds. "
            "<bookmark mark='c'/>His later theorems weakened the conditions further and further, and the "
            "impossibility remained. <bookmark mark='d'/>The Reasoner runs the experiment behind such theorems: six "
            "conditions, five views, and a search through small populations for a counterexample to each."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def search(self):
        d = load("arrhenius")
        t = d["table"]
        head = label(r"Six conditions, \ five views, \ searched", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        conds = ["quality", "mere addition", "non-anti-egalitarianism", "non-sadism", "negative addition", "dominance"]
        views = ["total", "average", "critical level", "variable value", "prioritarian"]
        assert d["violations"] == {"total": ["quality"],
                                   "average": ["mere addition", "non-sadism", "negative addition"],
                                   "critical level": ["mere addition", "non-sadism"],
                                   "variable value": ["mere addition", "non-sadism"],
                                   "prioritarian": ["quality"]}
        short = {"quality": r"\text{no repugnant}", "mere addition": r"\text{mere addition}",
                 "non-anti-egalitarianism": r"\text{equality}", "non-sadism": r"\text{non-sadism}",
                 "negative addition": r"\text{misery is bad}", "dominance": r"\text{dominance}"}
        hd = [r"\text{view}"] + [short[c] for c in conds]
        cells = [[label(v, font_size=17, color=WHITE)] + [mark(t[v][c]["holds"], 22) for c in conds] for v in views]
        grid = ValueGrid(hd, cells, col_w=[2.6, 2.0, 2.0, 1.5, 1.7, 2.0, 1.7], cell_h=0.5, font_size=16).move_to(
            [0, 0.55, 0])
        legend = stack([(r"no repugnant: \ no number of lives at 1 beats 10 lives at 10", GREY_A),
                        (r"mere addition: \ adding good lives that affect no one is not worse", GREY_A),
                        (r"non-sadism: \ adding good lives is never worse than adding miserable ones", GREY_A),
                        (r"misery is bad: \ adding lives not worth living makes things worse", GREY_A)],
                       font_size=16, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the search. <bookmark mark='a'/>The columns are six conditions: no repugnant conclusion, mere "
            "addition, a preference for equality among the same number of people, non-sadism, that adding miserable "
            "lives makes things worse, and dominance, that making everyone better off is better. "
            "<bookmark mark='b'/>The total view fails only the first. <bookmark mark='c'/>The average view fails three. "
            "<bookmark mark='d'/>Critical-level and variable-value views each fail two. <bookmark mark='e'/>And the "
            "prioritarian view fails the first, like the total view: putting more weight on the worse off does not "
            "stop numbers from outweighing quality. Every row has a cross; dominance and equality are the only "
            "columns everyone keeps."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule), *[FadeIn(grid.cell[k][0]) for k in range(5)])
            vo.wait_until("a")
            self.play(FadeIn(legend))
            for mk, ks in zip("bcde", ([0], [1], [2, 3], [4])):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for k in ks for c in grid.cell[k][1:]])
        self.clear_scene()

    def sadism(self):
        d = load("sadism")
        head = label(r"The sadistic conclusion", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["c"], d["base"], d["with_misery"], d["with_good_lives"]) == (2.0, 8.0, 5.0, 3.0)
        assert (d["total_with_misery"], d["total_with_good"]) == (9.0, 15.0)
        base_y = -1.0
        left = parfit_bars([(1, 10)], -6.2, base_y, unit_w=0.6, unit_h=0.2, color=WELL)
        neg = parfit_bars([(1, -1)], -5.5, base_y, unit_w=0.6, unit_h=0.2, color=RISK)
        right = parfit_bars([(1, 10)], -2.4, base_y, unit_w=0.6, unit_h=0.2, color=WELL)
        pos = parfit_bars([(5, 1)], -1.7, base_y, unit_w=0.6, unit_h=0.2, color=POP)
        axis = VGroup(Line([-6.4, base_y, 0], [-4.6, base_y, 0], color=GREY_B),
                      Line([-2.6, base_y, 0], [1.4, base_y, 0], color=GREY_B))
        la = label(r"add one life at $-1$", font_size=18, color=RISK).next_to(left, DOWN, buff=0.6).shift(RIGHT * 0.4)
        lb = label(r"add five lives at 1", font_size=18, color=POP).next_to(right, DOWN, buff=0.6).shift(RIGHT * 1.4)
        va = label(r"critical level 2: \ 5", font_size=18, color=GOAL).next_to(la, DOWN, buff=0.15)
        vb = label(r"critical level 2: \ 3", font_size=18, color=GOAL).next_to(lb, DOWN, buff=0.15)
        side = stack([(r"each life below $c$ counts against: \ $1 - 2 = -1$, \ five times", RISK),
                      (r"one life of misery costs only $-1 - 2 = -3$", RISK),
                      (r"so adding misery is better than adding good lives", BAD),
                      (r"the total view says the opposite: \ 15 against 9", WELL)],
                     font_size=19, aligned_edge=LEFT, width=4.6, buff=0.3).move_to([4.4, 0.0, 0])
        with self.voiceover(
            "One of Arrhenius's conditions deserves a closer look. <bookmark mark='a'/>Start with one person at ten. "
            "Compare adding one life of misery, at minus one, with adding five lives worth living, at one. "
            "<bookmark mark='b'/>On a critical-level view with level two, each of the five good lives counts as "
            "minus one, because it falls short of two: five in all. <bookmark mark='c'/>The miserable life counts "
            "as minus three. So adding misery scores five, and adding good lives scores three. "
            "<bookmark mark='d'/>The view prefers to add a miserable life rather than five lives worth living. "
            "Arrhenius called this the sadistic conclusion, and every critical-level view with a positive level "
            "implies it. <bookmark mark='e'/>The total view says the opposite, fifteen against nine. Avoiding the "
            "repugnant conclusion with a critical level buys the sadistic one."
        ) as vo:
            self.play(FadeIn(head), Create(axis))
            vo.wait_until("a")
            self.play(GrowFromEdge(left, DOWN), GrowFromEdge(right, DOWN))
            self.play(GrowFromEdge(neg, UP), FadeIn(la), GrowFromEdge(pos, DOWN), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(va), FadeIn(vb))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def examples(self):
        d = load("arrhenius")
        t = d["table"]
        head = label(r"The counterexamples the search found", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        ex = [("total", "quality"), ("average", "mere addition"), ("average", "negative addition"),
              ("critical level", "non-sadism"), ("variable value", "mere addition")]
        assert t["total"]["quality"]["example"] == "1000 lives at 1 beat 10 lives at 10"
        assert t["average"]["negative addition"]["example"] == "adding 1 at -1 to 1 at -2 makes it better"
        assert t["critical level"]["non-sadism"]["example"] == "adding 1 at -1 beats adding 5 at 1, to 1 at 10"
        assert t["average"]["mere addition"]["example"] == "adding 1 at 8 to 1 at 10 makes it worse"
        assert t["variable value"]["mere addition"]["example"] == "adding 20 at 1 to 10 at 10 makes it worse"
        cols = {"total": WELL, "average": POP, "critical level": RISK, "variable value": FUT}
        rows = [(f"{v}: \\ {c}", t[v][c]["example"].replace("-", "$-$"), cols[v]) for v, c in ex]
        g = rows_table(rows, top=1.6, gap=0.45, width=7.0, x_text=-0.6, label_size=19, text_size=19)
        foot = label(r"populations of 1 to 20 people at levels from $-4$ to 10; \ 1000 found by trying powers of ten",
                     font_size=17, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "And here are some of the counterexamples it found. <bookmark mark='a'/>For the total view, a thousand "
            "lives at one beat ten lives at ten: the repugnant conclusion in miniature. <bookmark mark='b'/>For the "
            "average view, adding one person at eight to a world of one person at ten makes it worse. "
            "<bookmark mark='c'/>Worse still, adding a miserable life at minus one to a hell of one person at minus "
            "two makes it better, since it raises the average. <bookmark mark='d'/>For a critical level of two, "
            "adding one miserable life is better than adding five lives worth living at one: the sadistic conclusion. "
            "<bookmark mark='e'/>And for variable value, adding twenty lives at one to ten lives at ten makes things "
            "worse. Each condition can be kept, but not all of them at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=36, current=36).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(36, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the thirty sixth brick in the Wall. <bookmark mark='a'/>The dream was an axiology for "
            "populations that meets every adequacy condition: one that avoids the repugnant conclusion, never prefers "
            "misery, and respects mere addition and equality. Arrhenius's impossibility theorems show there is none. "
            "<bookmark mark='b'/>What it forces is a choice of which repugnant-seeming conclusion to accept; a "
            "growing number of population ethicists now accept Parfit's as the least bad."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[36], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()
