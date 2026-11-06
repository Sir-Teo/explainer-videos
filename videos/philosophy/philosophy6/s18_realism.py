from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Realism(VoiceoverScene):
    def construct(self):
        card = chapter_card(17, r"Does CH have an answer?", r"When the axioms run out, is there still a fact?",
                            lit=(1947, 2012), part=PART)
        with self.voiceover("Chapter seventeen. Does the continuum hypothesis have an answer?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.godel()
        self.maddy()
        self.price_list()
        self.views()

    def godel(self):
        hc = history_card(1947, r"Kurt Gödel", r"`What is Cantor's continuum problem?'", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        q = quote_card(r"The set-theoretical concepts and theorems describe some well-determined reality, in which "
                       r"Cantor's conjecture must be either true or false.", r"Gödel (1947, rev.\ 1964)", width=10.6,
                       font_size=26).move_to([0, 0.5, 0])
        pts = VGroup(label(r"undecidability shows only that the axioms are incomplete", font_size=24),
                     label(r"new axioms can be justified by intuition, \ or by their fruitfulness", font_size=24),
                     label(r"Gödel's own guess: \ CH is false", font_size=24, color=GOAL)).arrange(
            DOWN, buff=0.22).next_to(q, DOWN, buff=0.5)
        with self.voiceover(
            "Gödel himself was a realist about sets. <bookmark mark='a'/>In 1947, before Cohen, he wrote that the "
            "concepts of set theory describe a well-determined reality, in which Cantor's conjecture must be either "
            "true or false. <bookmark mark='b'/>Its independence would show only that the axioms are incomplete. We "
            "should look for new axioms, justified either by intuition or by their fruitful consequences. And he "
            "guessed that the continuum hypothesis is false."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.4))
        self.clear_scene()

    def maddy(self):
        hc = history_card(1988, r"Penelope Maddy", r"`Believing the axioms' I and II", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        cols = VGroup(
            VGroup(label(r"intrinsic", font_size=30, color=SETC),
                   label(r"follows from the concept of set", font_size=24),
                   label(r"the iterative conception: \ ZFC, \ small large cardinals", font_size=22, color=GREY_A)
                   ).arrange(DOWN, buff=0.25),
            VGroup(label(r"extrinsic", font_size=30, color=CARD),
                   label(r"justified by its consequences", font_size=24),
                   label(r"determinacy, \ Woodin cardinals: \ they unify and explain", font_size=22, color=GREY_A)
                   ).arrange(DOWN, buff=0.25)).arrange(RIGHT, buff=1.6).move_to([0, 0.0, 0])
        bar = Line(UP * 1.2, DOWN * 1.2, color=GREY_D).move_to(cols.get_center())
        nat = label(r"Maddy's naturalism: \ the methods of set theory, not metaphysics, decide what to believe",
                    font_size=24, color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Penelope Maddy's papers of 1988 sorted the reasons set theorists actually give. <bookmark mark='a'/>"
            "Some axioms are justified intrinsically: they follow from the concept of set, the iterative picture. "
            "ZFC is of this kind. <bookmark mark='b'/>Others are justified extrinsically, by their consequences: "
            "determinacy and the large cardinals behind it are believed because they unify, explain, and settle "
            "questions. <bookmark mark='c'/>Maddy's later naturalism says that the methods of set theory itself, "
            "not a prior metaphysics, should decide which axioms to adopt."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]), Create(bar))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(nat))
        self.clear_scene()

    def price_list(self):
        d = load("chprice")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(x) for x in d["mus"]], radius=2.4, width=4.4, font_size=22,
                       center=[0, -0.6, 0], title=r"The Price List: \ the continuum")
        bg = label(r"held fixed, \ a theorem: \ CH is independent of ZFC and of the known large cardinals",
                   font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        positions = [(("N",), r"new axioms", r"Gödel; \ Woodin: \ the search goes on", ),
                     (("R",), r"no fact of the matter", r"Hamkins's multiverse; \ Feferman"),
                     (("K",), r"unknowable truth", r"a realist pessimism: \ CH has an answer \ we may never prove")]
        assert sorted(tuple(x) for x in d["mcs"]) == sorted(p[0] for p in positions)
        with self.voiceover(
            "The debate can be laid out as a Price List. <bookmark mark='a'/>Three claims: the continuum hypothesis "
            "has a determinate truth value; every mathematical truth follows from axioms we are justified in "
            "accepting; and no new justified axiom will settle it. Given the theorem that it is independent of "
            "the axioms we have, the three are inconsistent. <bookmark mark='b'/>Gödel and Woodin deny the third: "
            "new axioms will be found. <bookmark mark='c'/>Hamkins and Feferman deny the first: there is no single "
            "fact to find. <bookmark mark='d'/>And one can deny the second: the hypothesis has an answer that we "
            "may never be able to prove, a realism without the guarantee of knowledge."
        ) as vo:
            self.play(FadeIn(pl.title), LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.25),
                      Create(pl.conflict))
            vo.wait_until("a")
            self.play(FadeIn(bg))
            for i, (mk, (mcs, name, who)) in enumerate(zip("bcd", positions)):
                vo.wait_until(mk)
                if i:
                    self.play(*pl.reset(), run_time=0.6)
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def views(self):
        head = label(r"Four views of the continuum", font_size=34, color=CONN).to_edge(UP, buff=0.45)
        rows = [(r"Woodin (2001)", r"$\Omega$-logic: \ $2^{\aleph_0} = \aleph_2$, \ CH false", BAD),
                (r"Woodin (2010s)", r"`Ultimate $L$': \ an $L$-like universe with all large cardinals, \ CH true", OK),
                (r"Hamkins (2012)", r"the multiverse: \ many universes of sets, \ CH true in some, false in others", GOAL),
                (r"Feferman (2011)", r"CH is not a definite mathematical problem", GREY_A)]
        tab = VGroup()
        for i, (a, b, c) in enumerate(rows):
            y = 1.6 - 0.95 * i
            l1 = label(a, font_size=26, color=c)
            l2 = label(b, font_size=24)
            l1.move_to([-6.1 + l1.width / 2, y, 0])
            l2.move_to([-2.9 + l2.width / 2, y, 0])
            tab.add(VGroup(l1, l2))
        moral = label(r"a mathematical question has become a philosophical one: \ what are sets?", font_size=26,
                      color=OK).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Today there are four main views. <bookmark mark='a'/>Hugh Woodin argued around 2001 that a new logic "
            "points to the continuum being aleph two, so the hypothesis is false. <bookmark mark='b'/>Later he "
            "changed course, toward a universe he calls Ultimate L, which would contain all the large cardinals and "
            "make the hypothesis true. <bookmark mark='c'/>Joel David Hamkins defends a multiverse: there are many "
            "universes of sets, each as real as the others, connected by forcing. The hypothesis is true in some "
            "and false in others, and we already know exactly how it behaves among them. "
            "<bookmark mark='d'/>And Solomon Feferman argued that it is not a definite mathematical problem at all. "
            "<bookmark mark='e'/>A question Hilbert put first in mathematics has become a question in philosophy: "
            "what are sets, and what makes a statement about them true?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(moral))
        self.clear_scene()
