from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Price(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"The Price List", r"What must go, \ and who gives it up?", part=PART)
        with self.voiceover("Chapter twelve. The Price List."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.price_list()
        self.compare()

    def price_list(self):
        d = load("bfprice")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(x) for x in d["mus"]], radius=2.6, width=3.5, font_size=21,
                       center=[0, -0.5, 0], title=r"The Price List: \ the Benacerraf--Field puzzle")
        positions = [(("A",), r"concrete numbers", r"Mill; \ Maddy (1990): \ we see sets of eggs"),
                     (("O",), r"structure without objects", r"Hellman: \ modal structuralism; \ Chihara"),
                     (("K",), r"a fiction", r"Field: \ we know what follows, \ not what is true"),
                     (("C",), r"a special access", r"Gödel's intuition; \ Hale \& Wright; \ Balaguer; \ Linnebo")]
        assert sorted(tuple(x) for x in d["mcs"]) == sorted(p_[0] for p_ in positions)
        with self.voiceover(
            "The whole debate fits one Price List. <bookmark mark='a'/>Four claims, each very plausible. 'Seven is "
            "prime' is about an object, the number seven. That object is abstract, outside space and time, with no "
            "causes. We know that seven is prime. And to know about objects, we need some connection to them that "
            "could explain why our beliefs are reliable. Together they are inconsistent, and the Reasoner confirms "
            "that any three are consistent. <bookmark mark='b'/>Give up abstractness, and numbers are concrete: "
            "John Stuart Mill made arithmetic a science of physical aggregates, and Penelope Maddy, in 1990, argued "
            "that we literally see small sets, such as the set of three eggs in a carton. <bookmark mark='c'/>Give "
            "up the objects: modal structuralism, and Charles Chihara's constructions, keep the truths and drop the "
            "things. <bookmark mark='d'/>Give up the knowledge: Field's fictionalism, for which we know only what "
            "follows from what. <bookmark mark='e'/>Or give up the demand for a connection: Gödel's intuition; the "
            "neo-logicists' knowledge by definition; Mark Balaguer's full-blooded platonism, on which every "
            "consistent theory describes some objects, so that consistency is all the access we need; and Øystein "
            "Linnebo's thin objects, whose existence asks almost nothing of the world."
        ) as vo:
            self.play(FadeIn(pl.title), LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.25),
                      Create(pl.conflict))
            for i, (mk, (mcs, name, who)) in enumerate(zip("bcde", positions)):
                vo.wait_until(mk)
                if i:
                    self.play(*pl.reset(), run_time=0.6)
                anims, centre = pl.position(mcs, name, who, width=2.7)
                self.play(*anims)
        self.clear_scene()

    def compare(self):
        head = label(r"Four answers, \ side by side", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        hd = [label(r"", font_size=22), label(r"numbers are", font_size=22, color=P.CLAIM),
              label(r"keeps", font_size=22, color=P.CLAIM), label(r"faces", font_size=22, color=P.CLAIM)]
        rows = [[label(r"concrete", font_size=24, color=CONCRETE), label(r"aggregates, \ sets of things", font_size=21),
                 label(r"knowledge by perception", font_size=21), label(r"$2^{\aleph_0}$ eggs? \ the infinite", font_size=21)],
                [label(r"modal", font_size=24, color=OK), label(r"places in possible structures", font_size=21),
                 label(r"truth, \ no abstract objects", font_size=21), label(r"knowing what is possible", font_size=21)],
                [label(r"fiction", font_size=24, color=NUM), label(r"characters in a story", font_size=21),
                 label(r"ontology of physics", font_size=21), label(r"why the story applies", font_size=21)],
                [label(r"platonism", font_size=24, color=ABSTRACT), label(r"abstract objects", font_size=21),
                 label(r"truth at face value", font_size=21), label(r"Field's reliability challenge", font_size=21)]]
        grid = ValueGrid(hd, rows, col_w=[2.2, 3.8, 3.6, 3.8], cell_h=0.85, font_size=22).move_to([0, -0.1, 0])
        moral = label(r"the modal answer moves the puzzle: \ how do we know what is \textit{possible}? \ (Part 22)",
                      font_size=24, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Side by side: <bookmark mark='a'/>the concrete view keeps knowledge by perception, and must explain the "
            "infinite: there are not enough eggs. The modal view keeps truth without abstract objects, and must "
            "explain how we know what structures are possible. Fiction keeps the bare ontology of physics, and must "
            "explain why a story should apply so well to the world: Wigner's puzzle again. And platonism keeps "
            "truth at face value, and must answer Field's challenge. <bookmark mark='b'/>No answer is free. Notice "
            "that the modal answer only moves the puzzle, to knowledge of possibility, which Part 22 takes up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(4)], lag_ratio=0.6), run_time=8)
            vo.wait_until("b")
            self.play(FadeIn(moral))
        self.clear_scene()
