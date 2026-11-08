from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


class Belief(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Belief reports", r"Does Lois believe that Clark Kent flies?", lit=(1979, 1986, 1989),
                            part=PART)
        with self.voiceover("Chapter thirteen. Belief reports."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.lois()
        self.price()
        self.pierre()
        self.wall_brick()

    def lois(self):
        head = label(r"Lois Lane's beliefs", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        man = Dot([0, 0.9, 0], radius=0.16, color=REF)
        mtag = label(r"one man", font_size=18, color=REF).next_to(man, DOWN, buff=0.12)
        n1 = label(r"`Superman'", font_size=24, color=NAME).move_to([-3.4, 1.7, 0])
        n2 = label(r"`Clark Kent'", font_size=24, color=NAME).move_to([3.4, 1.7, 0])
        a1 = Arrow(n1.get_right(), man.get_left(), buff=0.15, color=NAME)
        a2 = Arrow(n2.get_left(), man.get_right(), buff=0.15, color=NAME)
        s1 = VGroup(label(r"Lois believes that Superman flies", font_size=24, color=SPEAK), tv(True, 26)).arrange(
            RIGHT, buff=0.4)
        s2 = VGroup(label(r"Lois believes that Clark Kent flies", font_size=24, color=SPEAK), tv(False, 26)).arrange(
            RIGHT, buff=0.4)
        pair = VGroup(s1, s2).arrange(DOWN, buff=0.3, aligned_edge=RIGHT).move_to([0, -0.9, 0])
        foot = label(r"swap co-referring names, \ and the report's truth value seems to change", font_size=22,
                     color=BAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Frege's puzzle returns in its sharpest form in reports of belief. <bookmark mark='a'/>Superman and "
            "Clark Kent are one man, with two names. <bookmark mark='b'/>Lois Lane believes that Superman flies. "
            "<bookmark mark='c'/>She would sincerely deny that Clark Kent flies; it seems false to say she believes "
            "it. <bookmark mark='d'/>So swapping co-referring names inside a belief report seems to change its truth "
            "value, just as in chapter two."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(man), FadeIn(mtag), FadeIn(n1), FadeIn(n2), GrowArrow(a1), GrowArrow(a2))
            vo.wait_until("b")
            self.play(FadeIn(s1))
            vo.wait_until("c")
            self.play(FadeIn(s2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def price(self):
        d = load("frege")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert sorted(d["mcs"]) == [["L"], ["N"], ["S"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.6, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ Frege's puzzle")
        positions = [(("N",), r"Frege", r"names have senses; \ in belief contexts they refer to them"),
                     (("L",), r"Salmon; \ Soames", r"she does believe Clark flies, \ under another guise; \ the "
                                                  r"report only sounds false"),
                     (("S",), r"Crimmins and Perry", r"reports carry a hidden mode of presentation: \ swapping names "
                                                     r"changes it")]
        with self.voiceover(
            "Three claims cannot all be true. <bookmark mark='a'/>A name's meaning is just its referent, as Mill and "
            "the direct-reference theorists say. Co-referring names can be swapped without changing a sentence's "
            "truth, given the first claim and compositionality. And Lois believes that Superman flies but does not "
            "believe that Clark Kent flies. <bookmark mark='b'/>Each position gives up one. "
            "<bookmark mark='c'/>Frege gives up the first: names have senses, and in belief reports they refer to "
            "them. <bookmark mark='d'/>The Russellians, Nathan Salmon in 1986 and Scott Soames, give up the third: "
            "strictly, Lois does believe that Clark Kent flies, under a guise she does not recognize, and the report "
            "only sounds false because of what it suggests. <bookmark mark='e'/>Mark Crimmins and John Perry, in "
            "1989, give up the second: a belief report says something about a mode of presentation that is not "
            "spelled out, so swapping names changes which mode is meant."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.2)
                self.play(*anims)
        self.clear_scene()

    def pierre(self):
        hc = history_card(1979, r"Saul Kripke", r"`A Puzzle about Belief'", width=5.2, color=HIST).to_corner(UL,
                                                                                                         buff=0.3)
        rows = [
            (r"in France", r"Pierre hears of a beautiful city: \ `Londres est jolie'", WORLD),
            (r"later", r"he moves to an ugly district of a city he learns to call `London': \ `London is not "
                       r"pretty'", SPEAK),
            (r"translation", r"so Pierre believes that London is pretty", REF),
            (r"disquotation", r"and Pierre believes that London is not pretty", REF),
            (r"the puzzle", r"no two names were swapped; \ only translation and disquotation: \ does he believe "
                            r"London is pretty, \ or not?", BAD),
        ]
        g = rows_table(rows, top=1.0, gap=0.42, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        foot = label(r"Kripke: \ every theory of belief must face this; \ none has a comfortable answer", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Kripke showed in 1979 that the problem is not just about substituting names. "
            "<bookmark mark='a'/>Pierre grows up in France and hears of a beautiful city. He says, sincerely, "
            "Londres est jolie. <bookmark mark='b'/>Later he moves, without realizing it, to an ugly district of the "
            "same city, which he learns to call London, and says London is not pretty. He never connects the two "
            "names. <bookmark mark='c'/>By translation, Pierre believes that London is pretty. "
            "<bookmark mark='d'/>By disquotation, Pierre believes that London is not pretty. "
            "<bookmark mark='e'/>No co-referring names were swapped; only two principles everyone uses. Yet Pierre "
            "is no fool, and does not hold contradictory beliefs in any ordinary sense. <bookmark mark='f'/>Kripke "
            "concluded that every theory of belief reports faces the puzzle, and none has a comfortable answer."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=27, current=27).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(27, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the twenty-seventh brick in the Wall. <bookmark mark='a'/>The dream was that meaning is "
            "reference: that a name contributes only its bearer, and a sentence only its truth conditions. Frege's "
            "puzzle, sharpened by belief reports, and Kripke's modal argument, which rules out the easy rescue by "
            "descriptions, stand in the way. <bookmark mark='b'/>The way through costs something: senses, with their "
            "shifting references, or Russellian meanings, with reports that are true when they sound false, or a "
            "hidden layer of context."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[27], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()
