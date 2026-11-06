from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Price(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"The Price List", r"What must go, and who gives it up?", part=PART)
        with self.voiceover("Chapter twelve. The Price List."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.price_list()
        self.compare()

    def price_list(self):
        d = load("liarprice")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(x) for x in d["mus"]], radius=2.5, width=4.0, font_size=21,
                       center=[0, -0.5, 0], title=r"The Price List: \ the liar")
        positions = [(("C",), r"a gap", r"Kripke; \ Field: \ give up excluded middle"),
                     (("N",), r"a glut", r"Priest: \ some contradictions are true"),
                     (("S",), r"a hierarchy", r"Tarski: \ no language contains its own truth"),
                     (("T",), r"a restriction", r"KF, \ Maudlin: \ classical logic, \ fewer T-sentences")]
        assert sorted(tuple(x) for x in d["mcs"]) == sorted(p_[0] for p_ in positions)
        with self.voiceover(
            "The whole debate fits one Price List. <bookmark mark='a'/>Four claims, each very plausible: classical "
            "logic; the T-schema for every sentence; a language that can say 'this sentence is not true'; and no "
            "true contradictions. Together, the liar shows, they are inconsistent, and any three are consistent. "
            "<bookmark mark='b'/>Kripke and Field give up classical logic: the gap. <bookmark mark='c'/>Priest gives "
            "up consistency: the glut. <bookmark mark='d'/>Tarski gives up self-reference within one language: the "
            "hierarchy. <bookmark mark='e'/>And the classical theories, such as the Kripke-Feferman theory or Tim "
            "Maudlin's, give up some instances of the T-schema: for them the liar is not true, and yet 'the liar is "
            "not true' is not true either."
        ) as vo:
            self.play(FadeIn(pl.title), LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.25),
                      Create(pl.conflict))
            for i, (mk, (mcs, name, who)) in enumerate(zip("bcde", positions)):
                vo.wait_until(mk)
                if i:
                    self.play(*pl.reset(), run_time=0.6)
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def compare(self):
        head = label(r"Four answers, \ side by side", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        hd = [label(r"", font_size=22), label(r"the liar", font_size=22, color=P.CLAIM),
              label(r"keeps", font_size=22, color=P.CLAIM), label(r"faces", font_size=22, color=P.CLAIM)]
        rows = [[label(r"gap", font_size=24, color="#8A93A6"), label(r"neither", font_size=22),
                 label(r"T-schema, \ consistency", font_size=21), label(r"`not determinately true'", font_size=21)],
                [label(r"glut", font_size=24, color=GLUT), label(r"both", font_size=22),
                 label(r"T-schema, \ excluded middle", font_size=21), label(r"`just true'; \ Curry", font_size=21)],
                [label(r"hierarchy", font_size=24, color=GOAL), label(r"cannot be said", font_size=22),
                 label(r"classical logic, \ T-schema per level", font_size=21), label(r"one word `true'", font_size=21)],
                [label(r"restriction", font_size=24, color=OK), label(r"not true, \ yet asserted", font_size=22),
                 label(r"classical logic", font_size=21), label(r"`$L$ is not true' \ is not true", font_size=21)]]
        grid = ValueGrid(hd, rows, col_w=[2.2, 2.6, 4.2, 4.0], cell_h=0.85, font_size=22).move_to([0, -0.1, 0])
        moral = label(r"no free lunch: \ every answer pays somewhere, \ and the revenge follows the payment",
                      font_size=24, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Side by side: <bookmark mark='a'/>the gap makes the liar neither, keeps the T-schema and consistency, "
            "and faces 'not determinately true'. The glut makes it both, keeps the schema and excluded middle, and "
            "faces 'just true' and Curry. The hierarchy cannot even say the liar, and loses the single word "
            "'true'. And the restriction asserts that the liar is not true, keeps classical logic, and must accept "
            "that what it says about the liar, it cannot call true. <bookmark mark='b'/>No answer is free, and in "
            "each case the revenge arrives exactly where the price was paid."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(4)], lag_ratio=0.6), run_time=8)
            vo.wait_until("b")
            self.play(FadeIn(moral))
        self.clear_scene()
