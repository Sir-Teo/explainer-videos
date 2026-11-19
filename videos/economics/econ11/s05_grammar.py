from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

GAMES = (
    ("coordination", r"coordination", (r"east quay", r"west quay"), r"which side of the road, \ which plug: \\ any "
     r"convention will do, \ if everyone keeps it", COOP),
    ("battle", r"the battle of the sexes", (r"regatta", r"market"), r"agree on something, \ but each prefers \\ a "
     r"different something", ANA),
    ("chicken", r"chicken", (r"dare", r"swerve"), r"two cars, \ one lane: \ each wants \\ the other to give way",
     DEFECT),
    ("stag", r"the stag hunt", (r"stag", r"hare"), r"the big prize needs both; \\ the safe one needs nobody", EQ),
)


class Grammar(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Coordination, \ the battle of the sexes, \ chicken \ and the stag hunt", r"How much of social "
             r"life fits into a two-by-two table?", "Chapter four. Coordination, the battle of the sexes, chicken "
             "and the stag hunt.", lit={1755: r"Rousseau's stag hunt"}, scale=("person", "nation"))
        self.four()
        self.lessons()

    def four(self):
        gr = load("grammar")
        tiles = VGroup()
        for key, name, acts, gloss, col in GAMES:
            g = gr[key]
            mat = matrix(g["A"], g["B"], acts, acts, row_name="", col_name="", cell_w=1.45, cell_h=0.7,
                         font_size=22, labels_size=16, highlight=[tuple(c) for c in g["pure"]])
            title = label(name, font_size=22, color=col)
            gl = label(gloss, font_size=16, color=GREY_A)
            tile = VGroup(title, mat, gl).arrange(DOWN, buff=0.18)
            tiles.add(tile)
        tiles.arrange_in_grid(rows=2, cols=2, buff=(0.9, 0.35)).move_to(DOWN * 0.1)
        if tiles.height > 7.3:
            tiles.scale_to_fit_height(7.3)
        note_ = label(r"gold frames: \ the pure equilibria", font_size=17, color=EQ).to_corner(DR, buff=0.25)
        tag = island_tag(corner=DL, font_size=15)
        with self.voiceover(
            "Four small games describe a surprising amount of social life. In a coordination "
            "game, both players simply want to match. The Island's boats can tie up at the east quay or the west, and "
            "it matters only that everyone uses the same one. Which side of the road to drive on is the same game. "
            "There are two equilibria, and history picks between them. <bookmark mark='b'/> The battle of the sexes "
            "adds a quarrel: both want to match, but each prefers a different meeting place. "
            "<bookmark mark='c'/> In chicken, two drivers race toward each other in one lane. Each wants the other to "
            "swerve; if neither does, both crash. The equilibria are the outcomes where exactly one swerves. "
            "<bookmark mark='d'/> And in Rousseau's stag hunt, two hunters can catch a stag only together, while "
            "either can catch a hare alone. Both hunting the stag is an equilibrium, and so is both settling for "
            "hares."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(note_), FadeIn(tiles[0], shift=UP * 0.1))
            for mk, t in zip("bcd", tiles[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.1))
        self.clear_scene()

    def lessons(self):
        head = label(r"what the four games teach", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"many games have several equilibria: \ the theory says what is stable, \ not which", font_size=25),
            label(r"the stag hunt: \ the better equilibrium is riskier, \ and needs trust", font_size=25, color=EQ),
            label(r"chicken: \ commitment wins, \ if you can make it visible \\ (throw the steering wheel out of the "
                  r"window)", font_size=24, color=DEFECT),
            label(r"coordination: \ conventions, \ standards, \ money itself, \ are equilibria someone chose",
                  font_size=25, color=COOP),
            label(r"which equilibrium people find: \ chapters 10 and 11", font_size=25, color=LEVEL),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Each teaches something. <bookmark mark='a'/> Most games worth studying have more than one equilibrium, "
            "and the theory says which outcomes are stable, not which one people will reach. "
            "<bookmark mark='b'/> In the stag hunt, the better equilibrium is the riskier one: hunt the stag and your "
            "partner wanders off, and you go hungry. It needs trust. <bookmark mark='c'/> In chicken, the player who "
            "can commit wins, if the commitment is visible: the classic image is a driver who throws the "
            "steering wheel out of the window. <bookmark mark='d'/> And conventions, standards, even money, are "
            "equilibria of coordination games that someone, or history, chose. <bookmark mark='e'/> How people find "
            "one equilibrium among many is the subject of chapters ten and eleven."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
