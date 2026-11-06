from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


def hull(planks, center, w=0.24, h=0.42, cols=10, orig=PARTC, new=WHOLE, empty=False):
    """A ship as a grid of planks: original planks one colour, replacements another."""
    g = VGroup()
    n = len(planks)
    rows = n // cols
    c = np.array(center, float)
    for i, p in enumerate(planks):
        r, k = divmod(i, cols)
        x = c[0] + (k - (cols - 1) / 2) * w
        y = c[1] + ((rows - 1) / 2 - r) * h
        if empty and not p:
            sq = Rectangle(width=w * 0.92, height=h * 0.9, stroke_width=0.8, stroke_color=GREY_D, fill_opacity=0)
        else:
            sq = Rectangle(width=w * 0.92, height=h * 0.9, stroke_width=0.8, stroke_color=GREY_B,
                           fill_color=(orig if (p if empty else not p) else new), fill_opacity=0.85)
        g.add(sq.move_to([x, y, 0]))
    keel = Polygon(c + np.array([-cols * w / 2 - 0.2, -rows * h / 2, 0]), c + np.array([cols * w / 2 + 0.2,
                                                                                        -rows * h / 2, 0]),
                   c + np.array([cols * w / 2 - 0.3, -rows * h / 2 - 0.35, 0]),
                   c + np.array([-cols * w / 2 + 0.3, -rows * h / 2 - 0.35, 0]), color=GREY_B, stroke_width=2)
    g.add(keel)
    return g


class Theseus(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"The ship of Theseus", r"Which ship is the original?", lit=(1655, 1980), part=PART)
        with self.voiceover("Chapter four. The ship of Theseus."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.replace()
        self.options()
        self.essentialism()
        self.real()

    def replace(self):
        d = load("theseus")
        head = label(r"Plank by plank \ (Plutarch; \ Hobbes, \ 1655)", font_size=30, color=CONN).to_edge(UP,
                                                                                                    buff=0.25)
        fr = d["frames"]
        A = hull(fr[0]["repaired"], [-3.6, 1.0, 0])
        B = hull(fr[0]["rebuilt"], [3.0, 1.0, 0], empty=True)
        la = label(r"ship A: \ repaired in the harbour", font_size=20, color=WHOLE).next_to(A, UP, buff=0.12)
        lb = label(r"ship B: \ rebuilt from the old planks", font_size=20, color=PARTC).next_to(B, UP, buff=0.12)
        ax = Axes(x_range=[0, d["planks"], 10], y_range=[0, 1, 0.5], x_length=5.6, y_length=1.6,
                  axis_config={"color": GREY_B, "font_size": 18}, x_axis_config={"include_numbers": True},
                  y_axis_config={"include_numbers": True}).move_to([-0.6, -2.0, 0])
        cA = series_plot(ax, d["share_repaired"], WHOLE, width=3)
        cB = series_plot(ax, d["share_rebuilt"], PARTC, width=3)
        axl = label(r"share of original planks", font_size=19, color=GREY_A).next_to(ax, UP, buff=0.05)
        dl = label(r"days", font_size=18, color=GREY_A).next_to(ax.x_axis, RIGHT, buff=0.1)
        key = VGroup(label(r"original plank", font_size=19, color=PARTC), label(r"new plank", font_size=19,
                                                                                 color=WHOLE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([-0.3, 1.0, 0])
        endA = label(r"ship A", font_size=19, color=WHOLE).next_to(ax.c2p(d["planks"], d["share_repaired"][-1]),
                                                                  UP, buff=0.3).shift(LEFT * 0.2)
        endB = label(r"ship B", font_size=19, color=PARTC).next_to(ax.c2p(d["planks"], d["share_rebuilt"][-1]),
                                                                  RIGHT, buff=0.15)
        with self.voiceover(
            "Plutarch tells of the ship of Theseus, kept by the Athenians as a memorial, whose rotting planks were "
            "replaced one by one, until philosophers argued over whether it was still the same ship. "
            "<bookmark mark='a'/>The Reasoner replaces one of its forty planks a day, in a random order. Ship A, in "
            "the harbour, keeps its shape and its use throughout. <bookmark mark='b'/>Thomas Hobbes added the twist. A "
            "scavenger keeps every discarded plank, and reassembles them, in their original places, into ship B. "
            "<bookmark mark='c'/>Day by day, the share of original planks in A falls, while B fills up. "
            "<bookmark mark='d'/>After forty days, A has no original plank at all, and B has every one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(la))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(axl), FadeIn(dl), FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(lb))
            vo.wait_until("c")
            for f in fr[1:4]:
                A2 = hull(f["repaired"], [-3.6, 1.0, 0])
                B2 = hull(f["rebuilt"], [3.0, 1.0, 0], empty=True)
                self.play(Transform(A, A2), Transform(B, B2), run_time=1.2)
            self.play(Create(cA), Create(cB), run_time=2)
            self.play(FadeIn(endA), FadeIn(endB))
            vo.wait_until("d")
            self.play(Transform(A, hull(fr[4]["repaired"], [-3.6, 1.0, 0])),
                      Transform(B, hull(fr[4]["rebuilt"], [3.0, 1.0, 0], empty=True)))
        self.clear_scene()

    def options(self):
        head = label(r"Which is the ship of Theseus?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"continuity", r"ship A: \ spatio-temporal and functional continuity; \ gradual replacement preserves "
                            r"identity", WHOLE),
            (r"composition", r"ship B: \ same planks in the same arrangement; \ a ship is its parts", PARTC),
            (r"both?", r"then A = B, \ but A and B are two ships in two places: \ transitivity forbids it", BAD),
            (r"best candidate", r"Nozick \ (1981): \ the closest continuer, \ if close enough; \ so whether A is "
                                r"Theseus's ship depends on whether B exists", GOAL),
            (r"no fact", r"Parfit's reading: \ every fact is known; \ `which is the real ship?' is an empty question",
             GREY_A),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Which is the ship of Theseus? <bookmark mark='a'/>Continuity favours A: it was never out of service, and "
            "replacement was gradual. <bookmark mark='b'/>Composition favours B: it is the same planks in the same "
            "arrangement. <bookmark mark='c'/>It cannot be both, for then A and B would be identical to each other, "
            "and they are two ships moored in two places. <bookmark mark='d'/>Robert Nozick's closest continuer "
            "theory says the original is whichever is the closest continuer, if it is close enough. A strange "
            "consequence: whether A is Theseus's ship depends on whether someone, elsewhere, builds B. "
            "<bookmark mark='e'/>Derek Parfit's moral: once we know every fact about the planks, which is the real "
            "ship is an empty question. The same structure returns with persons in chapter eleven."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def essentialism(self):
        d = load("theseus")
        head = label(r"How many ships were there?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        n = d["planks"]
        hd = [r"\text{view}", r"\text{ships over the 40 days}"]
        rows = [[MathTex(r"\text{continuity}", font_size=24, color=WHOLE), MathTex(r"1 \text{ (A), then B makes 2}",
                                                                                  font_size=24)],
                [MathTex(r"\text{mereological essentialism}", font_size=24, color=BAD),
                 MathTex(str(n + 1) + r"\text{: a new ship each day}", font_size=24)],
                [MathTex(r"\text{perdurance}", font_size=24, color=PARTC),
                 MathTex(r"\text{one worm, } " + str(n + 1) + r"\text{ daily stages}", font_size=24)],
                [MathTex(r"\text{nihilism (Part 20)}", font_size=24, color=GREY_A),
                 MathTex(r"0\text{: planks arranged ship-wise}", font_size=24)]]
        grid = ValueGrid(hd, rows, col_w=[5.0, 5.6], cell_h=0.62, font_size=20).move_to([0, 0.6, 0])
        notes = stack([(r"Chisholm \ (1973, \ 1976): \ a thing has its parts essentially; \ `same ship' is spoken "
                        r"loosely, \ of a succession", BAD),
                       (r"the counts differ by the answers of Part 20, \ applied over time", GOAL)], font_size=19,
                      width=12.0).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "How many ships were in the harbour over those forty days? <bookmark mark='a'/>On the continuity view, "
            "one, ship A, until the scavenger's ship B makes two. <bookmark mark='b'/>Roderick Chisholm held "
            "mereological essentialism: a thing has its parts essentially, so each replacement made a new ship. That "
            "is forty-one ships, and same ship is spoken only loosely, of a succession of ships. "
            "<bookmark mark='c'/>On perdurance, one worm, with forty-one daily stages. <bookmark mark='d'/>And on "
            "Part 20's nihilism, no ships at all, only planks arranged ship-wise. <bookmark mark='e'/>The counts "
            "differ exactly by the answers of Part 20, now applied across time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, i in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*grid.cell[i])))
                if i == 1:
                    self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.clear_scene()

    def real(self):
        head = label(r"Real ships of Theseus", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Ise Jingū", r"the shrine is rebuilt from new timber every twenty years, \ since the seventh century: "
                           r"\ the 62nd rebuilding was in 2013", WHOLE),
            (r"USS Constitution", r"launched 1797, \ still commissioned; \ only a small fraction of her timber is "
                                  r"original", UNIV),
            (r"your body", r"most of its atoms and many of its cells are replaced over years, \ though neurons largely "
                           r"persist", NOM),
            (r"a code base", r"every line rewritten over a decade, \ under one repository name and history", PARTC),
            (r"the verdicts", r"we follow form, \ function and history, \ and are untroubled by matter", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Ships of Theseus are everywhere. <bookmark mark='a'/>The great shrine at Ise in Japan is rebuilt from new "
            "timber every twenty years, a practice going back to the seventh century; the sixty-second rebuilding was "
            "in 2013, and it is still called the same shrine. <bookmark mark='b'/>The USS Constitution, launched in "
            "1797, is still a commissioned ship, though only a small fraction of her timber is original. "
            "<bookmark mark='c'/>Your own body replaces most of its atoms and many of its cells over the years, though "
            "most neurons last a lifetime. <bookmark mark='d'/>A software project may rewrite every line over a "
            "decade, under one name and one continuous history. <bookmark mark='e'/>In practice we track form, "
            "function and history, and are untroubled by the matter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
