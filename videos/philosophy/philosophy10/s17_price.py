from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Price(VoiceoverScene):
    def construct(self):
        card = chapter_card(16, r"The Price List", r"What must go, \ and who gives it up?", part=PART)
        with self.voiceover("Chapter sixteen. The Price List."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.price_list()
        self.compare()

    def price_list(self):
        d = load("empprice")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(x) for x in d["mus"]], radius=2.6, width=3.8, font_size=22,
                       center=[0, -0.6, 0], title=r"The Price List: \ the empiricist trilemma")
        positions = [(("E",), r"reason", r"Descartes, \ Leibniz: \ innate ideas; \ Kant: \ the mind's own forms"),
                     (("N",), r"no necessity", r"Mill: \ arithmetic is generalized experience; \ Quine (Part 11)"),
                     (("S",), r"seeing what must be", r"Aristotle: \ induction grasps essences; \ modern modal "
                                                     r"empiricists")]
        assert sorted(tuple(x) for x in d["mcs"]) == sorted(p_[0] for p_ in positions)
        with self.voiceover(
            "The part fits a Price List with three claims. <bookmark mark='a'/>All our knowledge comes from "
            "experience. We know some necessary truths: seven and five could not have made anything but twelve. And "
            "experience shows only what is, never what must be. The Reasoner confirms that the three are "
            "inconsistent, and any two consistent. <bookmark mark='b'/>Give up the first, and some knowledge comes "
            "from reason itself: Descartes's and Leibniz's innate ideas, or Kant's forms of intuition and categories. "
            "<bookmark mark='c'/>Give up the second: there is no necessary knowledge, only very well confirmed "
            "generalizations. John Stuart Mill said this of arithmetic, and Quine of everything, as Part 11 will "
            "show. <bookmark mark='d'/>Or give up the third: experience can show necessity. Aristotle held that "
            "induction lets us grasp the essences of things, and some modern philosophers think we learn what is "
            "possible from what we observe."
        ) as vo:
            self.play(FadeIn(pl.title), LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.25),
                      Create(pl.conflict))
            for i, (mk, (mcs, name, who)) in enumerate(zip("bcd", positions)):
                vo.wait_until(mk)
                if i:
                    self.play(*pl.reset(), run_time=0.6)
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def compare(self):
        head = label(r"Four answers, \ side by side", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        hd = [label(r"", font_size=22), label(r"necessary knowledge comes from", font_size=22, color=P.CLAIM),
              label(r"faces", font_size=22, color=P.CLAIM)]
        rows = [[label(r"rationalism", font_size=24, color=REASON), label(r"reason alone", font_size=22),
                 label(r"why should reason fit the world?", font_size=21)],
                [label(r"Kant", font_size=24, color=KANT), label(r"the mind's forms of experience", font_size=22),
                 label(r"non-Euclidean space; \ things in themselves", font_size=21)],
                [label(r"radical empiricism", font_size=24, color=SENSE), label(r"nowhere: \ there is none", font_size=22),
                 label(r"logic and mathematics seem necessary", font_size=21)],
                [label(r"Aristotelian", font_size=24, color=OK), label(r"experience of essences", font_size=22),
                 label(r"how could a few cases show `must'?", font_size=21)]]
        grid = ValueGrid(hd, rows, col_w=[3.0, 5.0, 5.2], cell_h=0.85, font_size=22).move_to([0, -0.2, 0])
        foot = label(r"Hume's problem, \ and Kant's price, \ are the tenth brick", font_size=24, color=P.WALL).to_edge(
            DOWN, buff=0.45)
        with self.voiceover(
            "Side by side: <bookmark mark='a'/>the rationalist gets necessary knowledge from reason alone, and must "
            "explain why reason should fit the world. Kant gets it from the mind's own forms, and must face "
            "non-Euclidean space, and the unknowable things in themselves. The radical empiricist says there is none, "
            "and must explain why logic and mathematics seem necessary. The Aristotelian gets it from experience of "
            "essences, and must explain how a few cases can show what must be so. <bookmark mark='b'/>That is the "
            "tenth brick in the Wall: Hume's problem, and the price of Kant's solution."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(4)], lag_ratio=0.6), run_time=8)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
